# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Functions to help save a trained model."""

import json
import os
import pickle
import shutil
import torch

from ...common.exceptions import AutoMLVisionValidationException
from ...object_detection.common import constants


def write_model(model_wrapper, output_dir, device=None, enable_onnx_norm=False):
    """Save a model to Artifacts

    :param model_wrapper: Wrapper that contains model
    :type model_wrapper: CommonObjectDetectionModelWrapper (see object_detection.models.base_model_wrapper)
    :param output_dir: Name of dir to save model files. If it does not exist, it will be created.
    :type output_dir: String
    :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
    :type device: str
    :param enable_onnx_norm: enable normalization when exporting onnx
    :type enable_onnx_norm: bool
    """
    os.makedirs(output_dir, exist_ok=True)

    # Explicitly Save the labels to a json file.
    if model_wrapper.names is None:
        raise AutoMLVisionValidationException('No labels is found in dataset wrapper', has_pii=False)
    label_file_path = os.path.join(output_dir, constants.ArtifactLiterals.LABEL_FILE_NAME)
    with open(label_file_path, 'w') as f:
        json.dump(model_wrapper.names, f)

    # Save PyTorch model weights
    model_location = os.path.join(output_dir,
                                  constants.ArtifactLiterals.MODEL_FILE_NAME)
    torch.save(model_wrapper.model.state_dict(), model_location)

    # Export and save the torch onnx model
    onnx_file_path = os.path.join(output_dir, constants.ArtifactLiterals.ONNX_MODEL_FILE_NAME)
    model_wrapper.export_onnx_model(file_path=onnx_file_path, device=device, enable_norm=enable_onnx_norm)

    # Save pickle file
    model_wrapper.model = None
    model_wrapper.device = None
    model_wrapper_location = os.path.join(output_dir,
                                          constants.ArtifactLiterals.PICKLE_FILE_NAME)

    with open(model_wrapper_location, "wb") as pickle_file:
        pickle.dump(model_wrapper, pickle_file)

    # Save score script
    dirname = os.path.dirname(os.path.abspath(__file__))
    shutil.copy(os.path.join(dirname, constants.ArtifactLiterals.SCORE_SCRIPT),
                os.path.join(output_dir, constants.ArtifactLiterals.SCORE_SCRIPT))
