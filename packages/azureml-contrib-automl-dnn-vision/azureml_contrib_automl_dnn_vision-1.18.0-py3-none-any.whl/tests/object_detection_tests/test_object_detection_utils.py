import os
import pytest
import tempfile
import unittest.mock as mock

import azureml.contrib.automl.dnn.vision.object_detection.common.object_detection_utils as od_utils
from azureml.contrib.automl.dnn.vision.object_detection.common.constants import OutputFields
from azureml.contrib.automl.dnn.vision.object_detection.data.datasets import AmlDatasetObjectDetectionWrapper
from azureml.contrib.automl.dnn.vision.object_detection.eval.vocmap import VocMap

from .run_mock import RunMock, ExperimentMock
from .aml_dataset_mock import AmlDatasetMock
from .test_datasets import TestAmlDatasetObjectDetectionWrapper


@pytest.mark.usefixtures('new_clean_dir')
class TestObjectDetectionUtils:

    @staticmethod
    def _setup_wrapper(only_one_file=False):
        ws_mock, test_dataset_id, _, _ = TestAmlDatasetObjectDetectionWrapper._build_dataset(only_one_file)
        wrapper_mock = AmlDatasetObjectDetectionWrapper(test_dataset_id,
                                                        workspace=ws_mock,
                                                        datasetclass=AmlDatasetMock)
        return ws_mock, test_dataset_id, wrapper_mock

    @staticmethod
    def _write_output_file(output_file, only_one_file=False):
        with open(output_file, 'w') as f:
            line1 = '{"filename": "a7c014ec-474a-49f4-8ae3-09049c701913-1.txt", ' \
                    '"boxes": [{"box": {"topX": 0.1, "topY": 0.9, "bottomX": 0.2, "bottomY": 0.8}, ' \
                    '"label": "cat", "score": 0.7}]}'
            line2 = '{"filename": "a7c014ec-474a-49f4-8ae3-09049c701913-2", ' \
                    '"boxes": [{"box": {"topX": 0.5, "topY": 0.5, "bottomX": 0.6, "bottomY": 0.4}, '\
                    '"label": "dog", "score": 0.8}]}'
            f.write(line1 + '\n')
            f.write(line2 + '\n')

    @mock.patch(od_utils.__name__ + '.AmlDatasetObjectDetectionWrapper')
    @mock.patch(od_utils.__name__ + '.VocMap')
    @mock.patch(od_utils.__name__ + '._parse_bounding_boxes')
    @mock.patch(od_utils.__name__ + '._evaluate_results')
    def test_validate_score_run(self, mock_eval, mock_parse, mock_vocmap, mock_wrapper):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            # Patch functions
            ws_mock, test_dataset_id, wrapper_mock = self._setup_wrapper()
            vocmap_obj = VocMap(wrapper_mock)

            mock_wrapper.return_value = wrapper_mock
            mock_vocmap.return_value = vocmap_obj
            mock_parse.return_value = 'mock_bounding_boxes'
            mock_eval.return_value = None

            # Setup mock objects
            predictions_file = 'predictions_od.txt'
            output_file = os.path.join(tmp_output_dir, predictions_file)
            experiment_mock = ExperimentMock(ws_mock)
            mock_run = RunMock(experiment_mock)

            od_utils._validate_score_run(input_dataset_id=test_dataset_id,
                                         workspace=ws_mock,
                                         output_file=output_file,
                                         score_run=mock_run)

            # Assert that expected methods were called
            mock_wrapper.assert_called_once_with(dataset_id=test_dataset_id, is_train=False,
                                                 ignore_data_errors=True, workspace=ws_mock,
                                                 download_files=False)
            mock_vocmap.assert_called_once_with(wrapper_mock)
            mock_parse.assert_called_once_with(output_file, wrapper_mock, wrapper_mock.classes)
            mock_eval.assert_called_once_with(mock_run, wrapper_mock, vocmap_obj, 'mock_bounding_boxes')

    def test_parse_bounding_boxes(self):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            # Setup output file
            predictions_file = 'predictions_od.txt'
            output_file = os.path.join(tmp_output_dir, predictions_file)
            self._write_output_file(output_file)

            _, _, wrapper_mock = self._setup_wrapper()
            eval_bounding_boxes = od_utils._parse_bounding_boxes(output_file=output_file,
                                                                 validation_dataset=wrapper_mock,
                                                                 val_index_map=wrapper_mock.classes)

            assert len(eval_bounding_boxes) == 2

            bbox1 = eval_bounding_boxes[0]
            assert 'a7c014ec-474a-49f4-8ae3-09049c701913-1' in bbox1['image_id']
            assert bbox1['category_id'] == 'cat'
            assert bbox1['score'] == 0.7
            assert len(bbox1['bbox']) == 4

            bbox2 = eval_bounding_boxes[1]
            assert 'a7c014ec-474a-49f4-8ae3-09049c701913-2' in bbox2['image_id']
            assert bbox2['category_id'] == 'dog'
            assert bbox2['score'] == 0.8
            assert len(bbox1['bbox']) == 4

    @mock.patch(od_utils.__name__ + '._read_image')
    def test_parse_bounding_boxes_invalid_img(self, mock_read_img):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            # Mock behavior for invalid images
            mock_read_img.return_value = None
            predictions_file = 'predictions_od.txt'
            output_file = os.path.join(tmp_output_dir, predictions_file)
            self._write_output_file(output_file, True)

            _, _, wrapper_mock = self._setup_wrapper()
            eval_bounding_boxes = od_utils._parse_bounding_boxes(output_file=output_file,
                                                                 validation_dataset=wrapper_mock,
                                                                 val_index_map=wrapper_mock.classes)
            # No boxes are returned for an invalid image
            assert len(eval_bounding_boxes) == 0

    @mock.patch(od_utils.__name__ + '.VocMap.compute')
    def test_evaluate_results(self, mock_compute):
        # Set up mock objects
        mock_compute.return_value = {
            VocMap.LABEL_METRICS: {1: {'test_val'}, 2: {'test_val'}, 3: {'test_val'}},
            VocMap.PRECISION: 0.7,
            VocMap.RECALL: 0.8,
            VocMap.MAP: 0.9
        }

        mock_record = {
            'image_id': 'test_id',
            'bbox': 'test_value',
            'category_id': 'some_label',
            'score': 1.0
        }
        mock_bboxes = [mock_record]

        ws_mock, _, wrapper_mock = self._setup_wrapper()
        experiment_mock = ExperimentMock(ws_mock)
        mock_run = RunMock(experiment_mock)
        vocmap_obj = VocMap(wrapper_mock)

        od_utils._evaluate_results(score_run=mock_run,
                                   validation_dataset=wrapper_mock,
                                   val_vocmap=vocmap_obj,
                                   eval_bounding_boxes=mock_bboxes)

        # Validate that compute was called
        mock_compute.assert_called_once_with(mock_bboxes)

        properties = mock_run.properties
        vocmap_result = properties[OutputFields.VOCMAP_RESULT]

        # Validate vocmap_result_with_classes was created properly
        assert len(vocmap_result) == 3
        assert 'cat' in vocmap_result
        assert 'dog' in vocmap_result
        assert 'pepsi_symbol' in vocmap_result

        # Validate properties and metrics contain expected values
        assert properties[VocMap.PRECISION] == 0.7
        assert properties[VocMap.RECALL] == 0.8
        assert properties[VocMap.MAP] == 0.9

        metrics = mock_run.metrics
        assert metrics[VocMap.PRECISION] == 0.7
        assert metrics[VocMap.RECALL] == 0.8
        assert metrics[VocMap.MAP] == 0.9
