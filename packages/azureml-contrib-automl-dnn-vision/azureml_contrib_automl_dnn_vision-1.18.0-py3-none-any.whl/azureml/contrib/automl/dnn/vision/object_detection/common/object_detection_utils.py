# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Common utilities for object detection and object detection yolo."""
import json
import os
import pickle
import time
import torch

from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from azureml.contrib.automl.dnn.vision.common.utils import _read_image
from azureml.contrib.automl.dnn.vision.object_detection.common import boundingbox
from azureml.core.experiment import Experiment
from azureml.core.run import Run

from .constants import ArtifactLiterals, OutputFields
from .masktools import convert_mask_to_polygon
from ..data.datasets import AmlDatasetObjectDetectionWrapper
from ..eval.utils import prepare_bounding_boxes_for_eval
from ..eval.vocmap import VocMap
from ...common.average_meter import AverageMeter
from ...common.system_meter import SystemMeter

logger = get_logger(__name__)


def _load_model_wrapper(torch_model_file, model_wrapper_pkl, **model_settings):
    with open(model_wrapper_pkl, 'rb') as fp:
        model_wrapper = pickle.load(fp)

    model_weights = torch.load(torch_model_file)
    model_wrapper.restore_model(model_weights, **model_settings)

    return model_wrapper


def _distill_run_from_experiment(run_id, experiment_name=None):
    current_experiment = Run.get_context().experiment
    experiment = current_experiment

    if experiment_name is not None:
        workspace = current_experiment.workspace
        experiment = Experiment(workspace, experiment_name)

    return Run(experiment=experiment, run_id=run_id)


def _fetch_model_from_artifacts(run_id, experiment_name=None, **model_settings):
    logger.info("Start fetching model from artifacts")
    run = _distill_run_from_experiment(run_id, experiment_name)

    run.download_file(os.path.join(ArtifactLiterals.OUTPUT_DIR, ArtifactLiterals.MODEL_FILE_NAME),
                      ArtifactLiterals.MODEL_FILE_NAME)
    run.download_file(os.path.join(ArtifactLiterals.OUTPUT_DIR, ArtifactLiterals.PICKLE_FILE_NAME),
                      ArtifactLiterals.PICKLE_FILE_NAME)
    logger.info("Finished downloading files from artifacts")

    return _load_model_wrapper(ArtifactLiterals.MODEL_FILE_NAME, ArtifactLiterals.PICKLE_FILE_NAME,
                               **model_settings)


def _get_box_dims(image_shape, box):
    box_keys = ['topX', 'topY', 'bottomX', 'bottomY']
    height, width = image_shape[0], image_shape[1]

    box_dims = dict(zip(box_keys, [coordinate.item() for coordinate in box]))

    box_dims['topX'] = box_dims['topX'] * 1.0 / width
    box_dims['bottomX'] = box_dims['bottomX'] * 1.0 / width
    box_dims['topY'] = box_dims['topY'] * 1.0 / height
    box_dims['bottomY'] = box_dims['bottomY'] * 1.0 / height

    return box_dims


def _get_bounding_boxes(label, image_shape, classes):
    bounding_boxes = []

    if 'masks' not in label:
        masks = [None] * len(label['boxes'])
    else:
        masks = label['masks']

    for box, label_index, score, mask in zip(label['boxes'], label['labels'], label['scores'], masks):
        box_dims = _get_box_dims(image_shape, box)

        box_record = {'box': box_dims,
                      'label': classes[label_index],
                      'score': score.item()}

        if mask is not None:
            mask = convert_mask_to_polygon(mask)
            box_record['polygon'] = mask

        bounding_boxes.append(box_record)

    return bounding_boxes


def _write_prediction_file_line(fw, filename, label, image_shape, classes):
    bounding_boxes = _get_bounding_boxes(label, image_shape, classes)

    annotation = {'filename': filename,
                  'boxes': bounding_boxes}

    fw.write('{}\n'.format(json.dumps(annotation)))


def _write_dataset_file_line(fw, filename, label, image_shape, classes):
    labels = []
    scores = []

    if 'masks' not in label:
        masks = [None] * len(label['boxes'])
    else:
        masks = label['masks']

    for box, label_index, score, mask in zip(label['boxes'], label['labels'], label['scores'], masks):
        label_record = _get_box_dims(image_shape, box)
        label_record['label'] = classes[label_index]

        if mask is not None:
            mask = convert_mask_to_polygon(mask)
            label_record['polygon'] = mask

        labels.append(label_record)
        scores.append(score.item())

    AmlLabeledDatasetHelper.write_dataset_file_line(
        fw,
        filename,
        scores,
        labels)


def _parse_bounding_boxes(output_file, validation_dataset, val_index_map):
    logger.info("Start parsing predictions.")
    prediction_lines = 0
    bounding_boxes = []
    with open(output_file) as od:
        for prediction_line in od:
            prediction_lines += 1
            prediction_dict = json.loads(prediction_line)

            filename = validation_dataset._labeled_dataset_helper.get_image_full_path(prediction_lines - 1)
            # Ensure we deal with the same files in validation dataset as output file
            assert prediction_dict['filename'] in filename

            image = _read_image(ignore_data_errors=True, image_url=filename)
            if image is None:
                logger.info("Skip invalid image {}.".format(image))
                continue

            height = image.height
            width = image.width

            image_boxes = boundingbox.ImageBoxes(filename, val_index_map)
            boxes = []
            labels = []
            scores = []
            for box in prediction_dict['boxes']:
                box_coordinates = [box['box']["topX"] * width, box['box']["topY"] * height,
                                   box['box']["bottomX"] * width, box['box']["bottomY"] * height]
                boxes.append(box_coordinates)
                labels.append(validation_dataset.label_to_index_map(box['label']))
                scores.append(box['score'])
            image_boxes.add_boxes(torch.tensor(boxes), torch.tensor(labels), torch.tensor(scores))
            bounding_boxes.append(image_boxes)

    logger.info("End parsing {} predictions.".format(prediction_lines))
    return prepare_bounding_boxes_for_eval(bounding_boxes)


def _evaluate_results(score_run, validation_dataset, val_vocmap, eval_bounding_boxes):
    voc_metric_time = AverageMeter()
    voc_metric_start = time.time()

    vocmap_result = val_vocmap.compute(eval_bounding_boxes)

    voc_metric_time.update(time.time() - voc_metric_start)

    vocmap_score = vocmap_result[VocMap.MAP]
    precision = vocmap_result[VocMap.PRECISION]
    recall = vocmap_result[VocMap.RECALL]

    vocmap_result_with_classes = {}
    for k, v in vocmap_result[VocMap.LABEL_METRICS].items():
        vocmap_result_with_classes[validation_dataset.index_to_label(k)] = v

    logger.info("Voc map result: {}".format(vocmap_result_with_classes))
    logger.info("Voc map score: {}".format(round(vocmap_score, 3)))
    logger.info("Precision: {}".format(round(precision, 3)))
    logger.info("Recall: {}".format(round(recall, 3)))
    logger.info("Voc Time {voc_time.value:.4f} ({voc_time.avg:.4f})".format(
        voc_time=voc_metric_time))

    score_run.log(VocMap.MAP, round(vocmap_score, 3))
    score_run.log(VocMap.PRECISION, round(precision, 3))
    score_run.log(VocMap.RECALL, round(recall, 3))
    properties_to_add = {
        OutputFields.VOCMAP_RESULT: vocmap_result_with_classes,
        VocMap.MAP: vocmap_score,
        VocMap.PRECISION: precision,
        VocMap.RECALL: recall
    }
    score_run.add_properties(properties_to_add)


def _validate_score_run(input_dataset_id, workspace, output_file, score_run):
    logger.info("Begin validating scoring run")
    if input_dataset_id is None:
        logger.warning("No input dataset specified, skipping validation.")
        return

    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    logger.info("Initializing validation dataset.")
    try:
        validation_dataset = AmlDatasetObjectDetectionWrapper(dataset_id=input_dataset_id,
                                                              is_train=False,
                                                              ignore_data_errors=True,
                                                              workspace=workspace,
                                                              download_files=False)
    except KeyError:
        logger.warning("Dataset does not contain ground truth, skipping validation.")
        return
    logger.info("End initializing validation dataset.")

    val_vocmap = VocMap(validation_dataset)
    val_index_map = validation_dataset.classes

    # Parse the predictions
    eval_bounding_boxes = _parse_bounding_boxes(output_file, validation_dataset, val_index_map)
    # Compare the results
    _evaluate_results(score_run, validation_dataset, val_vocmap, eval_bounding_boxes)
