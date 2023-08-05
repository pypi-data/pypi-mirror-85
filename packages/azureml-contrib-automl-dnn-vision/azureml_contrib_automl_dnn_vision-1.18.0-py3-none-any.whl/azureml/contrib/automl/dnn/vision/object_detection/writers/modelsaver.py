# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Functions to help save a trained model."""

import os
import pickle
import shutil
import torch
import json

from ..common.constants import ArtifactLiterals
from ...common.exceptions import AutoMLVisionValidationException


def write_model(model_wrapper, labels, output_dir,
                device=None, enable_onnx_norm=False):
    """Save a model to Artifacts

    :param model_wrapper: Wrapper that contains model
    :type model_wrapper: CommonObjectDetectionModelWrapper (see object_detection.models.base_model_wrapper)
    :param labels: list of classes
    :type labels: list
    :param output_dir: Name of dir to save model files. If it does not exist, it will be created.
    :type output_dir: String
    :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
    :type device: str
    :param enable_onnx_norm: enable normalization when exporting onnx
    :type enable_onnx_norm: bool
    """
    os.makedirs(output_dir, exist_ok=True)

    # Export and save the torch onnx model.
    onnx_file_path = os.path.join(output_dir, ArtifactLiterals.ONNX_MODEL_FILE_NAME)
    model_wrapper.export_onnx_model(file_path=onnx_file_path, device=device, enable_norm=enable_onnx_norm)

    # Explicitly Save the labels to a json file.
    if labels is None:
        raise AutoMLVisionValidationException('No labels is found in dataset wrapper', has_pii=False)
    label_file_path = os.path.join(output_dir, ArtifactLiterals.LABEL_FILE_NAME)
    with open(label_file_path, 'w') as f:
        json.dump(labels, f)

    # Save PyTorch model weights
    model_location = os.path.join(output_dir, ArtifactLiterals.MODEL_FILE_NAME)
    torch.save(model_wrapper.get_state_dict(), model_location)

    # Save pickle file
    model_wrapper.model = None
    model_wrapper.device = None
    model_wrapper.distributed = False
    model_wrapper_location = os.path.join(output_dir, ArtifactLiterals.PICKLE_FILE_NAME)

    with open(model_wrapper_location, "wb") as pickle_file:
        pickle.dump(model_wrapper, pickle_file)

    # Save score script
    dirname = os.path.dirname(os.path.abspath(__file__))
    shutil.copy(os.path.join(dirname, ArtifactLiterals.SCORE_SCRIPT),
                os.path.join(output_dir, ArtifactLiterals.SCORE_SCRIPT))
