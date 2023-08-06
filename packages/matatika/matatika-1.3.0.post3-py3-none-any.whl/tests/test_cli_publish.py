'''CLI publish test module'''

from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import PropertyMock
import json
import random
import uuid
import yaml
from matatika.cli import matatika
from matatika.dataset import Dataset
from tests.test_cli import TestCLI


class TestCLIPublish(TestCLI):
    '''Test class for CLI publish command'''

    def test_publish_without_dataset_file_arg(self):
        '''Test publish without dataset file argument'''

        result = self.runner.invoke(matatika, ["publish"])
        self.assertIn("Error: Missing argument 'DATASET_FILE'.", result.output)
        self.assertIs(result.exit_code, 2)

    def test_publish_with_invalid_dataset_file_arg(self):
        '''Test publish with invalid dataset file argument'''

        invalid_path = "invalid-path"

        result = self.runner.invoke(matatika, ["publish",
                                               invalid_path])
        self.assertIn(f"Invalid value for 'DATASET_FILE': Path '{invalid_path}' does "
                      "not exist", result.output)
        self.assertIs(result.exit_code, 2)

    @patch('catalog.requests.post')
    @patch('catalog.jwt.decode', return_value=TestCLI.MOCK_DECODED_JWT)
    @patch('cli.MatatikaConfig.get_default_workspace', return_value=TestCLI.MOCK_WORKSPACES[0])
    @patch('cli.MatatikaConfig.get_endpoint_url', return_value='endpoint url')
    def test_publish(self, _mock_endpoint_url, __mock_default_workspace, _mock_decoded_jwt,
                     mock_post_request):
        '''Test publish'''

        package_dir = Path(__file__).parent.absolute()
        file_path = package_dir.joinpath('test_data/helloworld.yaml')

        with open(file_path, 'r') as datasets_yaml:
            datasets_dict = yaml.safe_load(datasets_yaml)['datasets']

        datasets = []
        mock_responses = []
        for alias in datasets_dict:
            dataset = Dataset.from_dict(datasets_dict[alias])
            dataset.dataset_id = str(uuid.uuid4())
            dataset.alias = alias
            datasets.append(dataset)

            mock_response = MagicMock()
            type(mock_response).status_code = PropertyMock(
                return_value=random.choice([200, 201]))
            mock_response.json.return_value = json.loads(dataset.to_json())
            mock_responses.append(mock_response)

        mock_post_request.side_effect = mock_responses

        result = self.runner.invoke(matatika, ["publish",
                                               str(file_path)])

        self.assertIn(f"Successfully published {len(datasets)} dataset(s)",
                      result.output)

        for dataset in datasets:
            self.assertIn(dataset.dataset_id, result.output)
            self.assertIn(dataset.alias, result.output)
            self.assertIn(dataset.title, result.output)
