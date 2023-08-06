'''Dataset test module'''

from pathlib import Path
import json
import sys
import unittest
import yaml
from matatika.dataset import Dataset

sys.path.append('../src/')


class TestDataset(unittest.TestCase):
    '''Test class for dataset operations'''

    def test_dataset_with_no_values(self):
        """
        Creates an empty dataset, converts it to JSON and then back to a Python object

        Expects returned object to be empty
        """

        dataset = Dataset()

        data = json.loads(dataset.to_json())

        self.assertFalse(data)

    def test_dataset_with_all_values(self):
        """
        Creates a populated dataset, converts it to JSON and then back to a Python object

        Expects each field to have the value that was initially set
        """

        dataset = Dataset()
        dataset.dataset_id = 'dataset-id'
        dataset.workspace_id = 'workspace-id'
        dataset.title = 'title'
        dataset.description = 'description'
        dataset.questions = 'questions'
        dataset.raw_data = 'raw-data'
        dataset.visualisation = 'visualisation'
        dataset.metadata = 'metadata'
        dataset.query = 'query'

        data = json.loads(dataset.to_json())

        self.assertEqual(data.get('id'),  dataset.dataset_id)
        self.assertEqual(data.get('workspaceId'),  dataset.workspace_id)
        self.assertEqual(data.get('title'), dataset.title)
        self.assertEqual(data.get('description'), dataset.description)
        self.assertEqual(data.get('questions'), dataset.questions)
        self.assertEqual(data.get('rawData'), dataset.raw_data)
        self.assertEqual(data.get('visualisation'), dataset.visualisation)
        self.assertEqual(data.get('metadata'), dataset.metadata)
        self.assertEqual(data.get('query'), dataset.query)

    def test_dataset_with_partial_values(self):
        """
        Creates a dataset with 'dataset-id' populated, converts it to JSON and then back to a
        Python object

        Expects the 'dataset-id' field to have the value that was initially set
        """

        dataset = Dataset()
        dataset.dataset_id = 'test-dataset'

        data = json.loads(dataset.to_json())

        self.assertEqual(data.get('id'), dataset.dataset_id)

        self.assertNotIn('workspaceId', data)
        self.assertNotIn('title', data)
        self.assertNotIn('description', data)
        self.assertNotIn('questions', data)
        self.assertNotIn('rawData', data)
        self.assertNotIn('visualisation', data)
        self.assertNotIn('metadata', data)
        self.assertNotIn('query', data)

    def test_to_json_all_fields(self):
        '''Tests to_json behaviour with all fields'''

        dataset = Dataset()
        dataset.dataset_id = 'dataset-id'
        dataset.alias = 'alias'
        dataset.workspace_id = 'workspace-id'
        dataset.title = 'title'
        dataset.description = 'description'
        dataset.questions = 'questions'
        dataset.raw_data = 'raw-data'
        dataset.visualisation = 'visualisation'
        dataset.metadata = 'metadata'
        dataset.query = 'query'

        dataset_str = \
            '{' \
            f'"id": "{dataset.dataset_id}", ' \
            f'"alias": "{dataset.alias}", ' \
            f'"workspaceId": "{dataset.workspace_id}", ' \
            f'"title": "{dataset.title}", ' \
            f'"description": "{dataset.description}", ' \
            f'"questions": "{dataset.questions}", ' \
            f'"rawData": "{dataset.raw_data}", ' \
            f'"visualisation": "{dataset.visualisation}", ' \
            f'"metadata": "{dataset.metadata}", ' \
            f'"query": "{dataset.query}"' \
            '}'

        self.assertEqual(dataset.to_json(), dataset_str)

    def test_to_json_partial_fields(self):
        '''Tests to_json behaviour with partial fields'''

        dataset = Dataset()
        dataset.alias = 'alias'

        dataset_str = \
            '{' \
            f'"alias": "{dataset.alias}"' \
            '}'

        self.assertEqual(dataset.to_json(), dataset_str)

    def test_from_dict(self):
        '''Tests from_dict behaviour'''

        package_dir = Path(__file__).parent.absolute()
        file_path = package_dir.joinpath('test_data/helloworld.yaml')

        with open(file_path, 'r') as datasets_yaml:
            data = yaml.safe_load(datasets_yaml)['datasets']['hello-world']

        dataset = Dataset.from_dict(data)

        self.assertEqual(data.get('id'),  dataset.dataset_id)
        self.assertEqual(data.get('workspaceId'),  dataset.workspace_id)
        self.assertEqual(data.get('title'), dataset.title)
        self.assertEqual(data.get('description'), dataset.description)
        self.assertEqual(data.get('questions'), dataset.questions)
        self.assertEqual(data.get('rawData'), dataset.raw_data)
        self.assertEqual(data.get('visualisation'), dataset.visualisation)
        self.assertEqual(data.get('metadata'), dataset.metadata)
        self.assertEqual(data.get('query'), dataset.query)


if __name__ == '__main__':
    unittest.main()
