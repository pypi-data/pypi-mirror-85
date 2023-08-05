# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Classes that wrap training steps"""

import copy
import itertools
import json
import os
import time
import torch

from ..eval import cocotools
from ..eval.utils import prepare_bounding_boxes_for_eval
from ..eval.vocmap import VocMap
from ..common import boundingbox
from ..common.constants import ArtifactLiterals, TrainingParameters
from ...common import distributed_utils
from ...common.exceptions import AutoMLVisionSystemException
from ...common.logging_utils import get_logger
from ...common.system_meter import SystemMeter
from ...common.trainer.lrschedule import LRSchedulerUpdateType
from ...common.utils import _add_run_properties, _data_exception_safe_iterator, log_end_training_stats
from ...common.average_meter import AverageMeter

logger = get_logger(__name__)


class TrainSettings:
    """Settings for training."""

    def __init__(self, **kwargs):
        """
        :param kwargs: Optional training parameters. Currently supports
          -number_of_epochs: Number of epochs to train for (int)
          -max_patience_iterations: Number of epochs with no validation
          improvement before stopping.
          -primary_metric: Metric that is evaluated and logged by AzureML run object.
          -early_stop_delay_iterations: Number of epochs to wait before tracking validation
          improvement for early stopping.
        :type kwargs: dict
        """

        self._number_of_epochs = kwargs.get(
            "number_of_epochs", TrainingParameters.DEFAULT_NUMBER_EPOCHS)
        self._max_patience_iterations = kwargs.get(
            "max_patience_iterations", TrainingParameters.DEFAULT_PATIENCE_ITERATIONS)
        self.primary_metric = kwargs.get(
            "primary_metric", TrainingParameters.DEFAULT_PRIMARY_METRIC)
        self._early_stop_delay_iterations = kwargs.get(
            "early_stop_delay_iterations", TrainingParameters.DEFAULT_EARLY_STOP_DELAY_ITERATIONS)

    @property
    def number_of_epochs(self):
        """Get number of epochs

        :return: number_of_epochs
        :rtype: int
        """
        return self._number_of_epochs

    @property
    def max_patience_iterations(self):
        """Get number of patience iterations

        :return: max_patience_iterations
        :rtype: int
        """
        return self._max_patience_iterations

    @property
    def early_stop_delay_iterations(self):
        """Get number of iterations to wait before early stop logic is executed.

        :return: early_stop_delay_iterations
        :rtype: int
        """
        return self._early_stop_delay_iterations


def move_images_to_device(images, device):
    """Convenience function to move images to device (gpu/cpu).

    :param images: Batch of images
    :type images: Pytorch tensor
    :param device: Target device
    :type device: Pytorch device
    """

    return [image.to(device) for image in images]


def move_targets_to_device(targets, device):
    """Convenience function to move training targets to device (gpu/cpu)

    :param targets: Batch Training targets (bounding boxes and classes)
    :type targets: Dictionary
    :param device: Target device
    :type device: Pytorch device
    """

    return [{k: v.to(device) for k, v in target.items()} for
            target in targets]


def train_one_epoch(model, optimizer, scheduler, train_data_loader,
                    device, criterion, epoch, print_freq, system_meter):
    """Train a model for one epoch

    :param model: Model to be trained
    :type model: Pytorch nn.Module
    :param optimizer: Optimizer used in training
    :type optimizer: Pytorch optimizer
    :param scheduler: Learning Rate Scheduler wrapper
    :type scheduler: BaseLRSchedulerWrapper (see common.trainer.lrschedule)
    :param train_data_loader: Data loader for training data
    :type train_data_loader: Pytorch data loader
    :param device: Target device
    :type device: Pytorch device
    :param criterion: Loss function wrapper
    :type criterion: Object derived from BaseCriterionWrapper (see object_detection.train.criterion)
    :param epoch: Current training epoch
    :type epoch: int
    :param print_freq: How often you want to print the output
    :type print_freq: int
    :param system_meter: A SystemMeter to collect system properties
    :type system_meter: SystemMeter
    """

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()

    model.train()

    end = time.time()
    for i, (images, targets, info) in enumerate(_data_exception_safe_iterator(iter(train_data_loader))):
        # measure data loading time
        data_time.update(time.time() - end)

        images = move_images_to_device(images, device)
        targets = move_targets_to_device(targets, device)

        loss_dict = criterion.evaluate(model, images, targets)
        loss = sum(loss_dict.values())
        loss_value = loss.item()

        if distributed_utils.dist_available_and_initialized():
            # In distributed mode, aggregate loss from all processes for logging purposes.
            loss_dict_reduced = distributed_utils.reduce_dict(loss_dict)
            loss_reduced = sum(loss_dict_reduced.values())
            loss_value = loss_reduced.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if scheduler.update_type == LRSchedulerUpdateType.BATCH:
            scheduler.lr_scheduler.step()

        # record loss and measure elapsed time
        losses.update(loss_value, len(images))
        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_freq == 0 or i == len(train_data_loader) - 1:
            mesg = "Epoch: [{0}][{1}/{2}]\t" "lr: {3}\t" "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t"\
                   "Data {data_time.value:.4f} ({data_time.avg:.4f})\t" "Loss {loss.value:.4f} " \
                   "({loss.avg:.4f})\t".format(epoch, i, len(train_data_loader), optimizer.param_groups[0]["lr"],
                                               batch_time=batch_time, data_time=data_time, loss=losses)

            mesg += system_meter.get_gpu_stats()
            logger.info(mesg)
            system_meter.log_system_stats(True)

    if scheduler.update_type == LRSchedulerUpdateType.EPOCH:
        scheduler.lr_scheduler.step()


def validate(model, val_data_loader, device, val_index_map, system_meter):
    """Gets model results on validation set.

    :param model: Model to score
    :type mode: Pytorch nn.Module
    :param val_data_loader: Data loader for validation data
    :type val_data_loader: Pytorch Data Loader
    :param device: Target device
    :type device: Pytorch device
    :param val_index_map: Map from numerical indices to class names
    :type val_index_map: List of strings
    :returns: List of detections
    :rtype: List of ImageBoxes (see object_detection.common.boundingbox)
    :param system_meter: A SystemMeter to collect system properties
    :type SystemMeter
    """

    batch_time = AverageMeter()

    model.eval()

    bounding_boxes = []
    end = time.time()
    with torch.no_grad():
        for i, (images, targets, info) in enumerate(_data_exception_safe_iterator(iter(val_data_loader))):
            images = move_images_to_device(images, device)

            labels = model(images)

            for info, label in zip(info, labels):
                image_boxes = boundingbox.ImageBoxes(
                    info["filename"], val_index_map)

                image_boxes.add_boxes(label["boxes"],
                                      label["labels"],
                                      label["scores"],
                                      label.get("masks", None))

                bounding_boxes.append(image_boxes)

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if i % 100 == 0 or i == len(val_data_loader) - 1:
                mesg = "Test: [{0}/{1}]\t"\
                       "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t".format(i, len(val_data_loader),
                                                                                     batch_time=batch_time)
                mesg += system_meter.get_gpu_stats()
                logger.info(mesg)
                system_meter.log_system_stats(collect_only=True)

    return bounding_boxes


def train(model, optimizer, scheduler,
          train_data_loader, device, criterion,
          train_settings, val_data_loader, val_coco_index=None, val_vocmap=None,
          enable_coco_validation=False, val_index_map=None, run=None, ignore_data_errors=True):
    """Train a model

    :param model: Model to train
    :type model: Object derived from CommonObjectDetectionModelWrapper (see object_detection.models.base_model_wrapper)
    :param optimizer: Model Optimizer
    :type optimizer: Pytorch Optimizer
    :param scheduler: Learning Rate Scheduler wrapper.
    :type scheduler: BaseLRSchedulerWrapper (see common.trainer.lrschedule)
    :param train_data_loader: Data loader with training data
    :type train_data_loader: Pytorch data loader
    :param device: Target device (gpu/cpu)
    :type device: Pytorch Device
    :param criterion: Loss function
    :type criterion: Object dervied from CommonCriterionWrapper (see object_detection.train.criterion)
    :param train_settings: Settings for training.
    :type train_settings: TrainSettings object
    :param val_data_loader: Data loader with validation data.
    :type val_data_loader: Pytorch data loader
    :param val_coco_index (optional): Cocoindex created from validation data
    :type val_coco_index (optional): Pycocotool Cocoindex object
    :param val_vocmap (optional): VocMap created from validation data
    :type val_vocmap (optional): VocMap object
    :param enable_coco_validation (optional): enable validation and evaluation for every epoch using Pycocotools.
    :type enable_coco_validation (optional): bool
    :param val_index_map (optional): Map from class indices to class names
    :type val_index_map (optional): List of strings
    :param run: azureml run object
    :type run: azureml.core.run.Run
    :param ignore_data_errors: boolean flag to turn on or off errors due to missing or malformed input data
    :type ignore_data_errors: bool
    :returns: Trained model
    :rtype: Object derived from CommonObjectDetectionModelWrapper
    """
    epoch_time = AverageMeter()

    base_model = model.model

    distributed = distributed_utils.dist_available_and_initialized()
    master_process = distributed_utils.master_process()

    best_score = 0.0
    best_model = copy.deepcopy(model.get_state_dict())

    no_progress_counter = 0

    label_metrics = {}

    epoch_end = time.time()
    train_start = time.time()
    coco_metric_time = AverageMeter()
    voc_metric_time = AverageMeter()
    train_sys_meter = SystemMeter()
    valid_sys_meter = SystemMeter()
    for epoch in range(train_settings.number_of_epochs):
        logger.info("Training epoch {}.".format(epoch))

        if distributed:
            if train_data_loader.distributed_sampler is None:
                msg = "train_data_loader.distributed_sampler is None in distributed mode. " \
                      "Cannot shuffle data after each epoch."
                logger.error(msg)
                raise AutoMLVisionSystemException(msg, has_pii=False)
            train_data_loader.distributed_sampler.set_epoch(epoch)

        train_one_epoch(base_model, optimizer, scheduler,
                        train_data_loader, device, criterion, epoch,
                        print_freq=100, system_meter=train_sys_meter)

        bounding_boxes = validate(base_model, val_data_loader, device, val_index_map, valid_sys_meter)
        eval_bounding_boxes = prepare_bounding_boxes_for_eval(bounding_boxes)

        if distributed:
            # Gather eval bounding boxes from all processes.
            eval_bounding_boxes_list = distributed_utils.all_gather(eval_bounding_boxes)
            eval_bounding_boxes = list(itertools.chain.from_iterable(eval_bounding_boxes_list))

            logger.info("Gathered {} eval bounding boxes from all processes.".format(len(eval_bounding_boxes)))

        if not eval_bounding_boxes:
            logger.info("no detected bboxes for evaluation")

        if val_coco_index and enable_coco_validation:
            coco_metric_start = time.time()
            if "segmentation" in eval_bounding_boxes[0]:
                cocotools.score_from_index(val_coco_index, eval_bounding_boxes, "segm")
            else:
                cocotools.score_from_index(val_coco_index, eval_bounding_boxes)
            coco_metric_time.update(time.time() - coco_metric_start)
            logger.info("Coco Time {coco_time.value:.4f} ({coco_time.avg:.4f})".format(coco_time=coco_metric_time))

        if val_vocmap:
            voc_metric_start = time.time()
            vocmap_result = val_vocmap.compute(eval_bounding_boxes)
            voc_metric_time.update(time.time() - voc_metric_start)

            vocmap_score = vocmap_result[VocMap.MAP]
            precision = vocmap_result[VocMap.PRECISION]
            recall = vocmap_result[VocMap.RECALL]

            logger.info("Voc map result: {}".format(vocmap_result))
            logger.info("Voc map score: {}".format(round(vocmap_score, 3)))
            logger.info("Precision: {}".format(round(precision, 3)))
            logger.info("Recall: {}".format(round(recall, 3)))
            logger.info("Voc Time {voc_time.value:.4f} ({voc_time.avg:.4f})".format(voc_time=voc_metric_time))

            if epoch >= train_settings.early_stop_delay_iterations:
                # Start incrementing no progress counter only after early_stop_delay_iterations.
                no_progress_counter += 1

            if vocmap_score == best_score:
                best_model = copy.deepcopy(model.get_state_dict())
            elif vocmap_score > best_score:
                best_model = copy.deepcopy(model.get_state_dict())
                no_progress_counter = 0
                best_score = vocmap_score

            if master_process and run is not None:
                run.log(train_settings.primary_metric, round(vocmap_score, 3))
                run.log("precision", round(precision, 3))
                run.log("recall", round(recall, 3))

            for label, label_metric in vocmap_result[VocMap.LABEL_METRICS].items():
                label_name = val_index_map[label]
                if label_name not in label_metrics:
                    label_metrics[label_name] = {}
                for metric_name in [VocMap.PRECISION, VocMap.RECALL, VocMap.AVERAGE_PRECISION]:
                    if metric_name not in label_metrics[label_name]:
                        label_metrics[label_name][metric_name] = []
                    label_metrics[label_name][metric_name].append(round(label_metric[metric_name].item(), 3))
        else:
            best_model = copy.deepcopy(model.get_state_dict())

        # measure elapsed time
        epoch_time.update(time.time() - epoch_end)
        epoch_end = time.time()
        mesg = "Epoch-level: [{0}]\t" \
               "Epoch-level Time {epoch_time.value:.4f} ({epoch_time.avg:.4f})".format(epoch, epoch_time=epoch_time)
        logger.info(mesg)

        if no_progress_counter > train_settings.max_patience_iterations:
            break

    # measure total training time
    train_time = time.time() - train_start
    log_end_training_stats(train_time, epoch_time, train_sys_meter, valid_sys_meter)

    if master_process:
        model.load_state_dict(best_model)
        if run is not None:
            _add_run_properties(run, best_score)
        # Write label metrics to output file.
        output_dir = ArtifactLiterals.OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)
        label_metrics_file_path = os.path.join(output_dir, ArtifactLiterals.LABEL_METRICS_FILE_NAME)
        with open(label_metrics_file_path, 'w') as f:
            json.dump(label_metrics, f)
