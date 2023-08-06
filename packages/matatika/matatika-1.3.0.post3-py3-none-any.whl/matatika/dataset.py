# pylint: disable=too-many-instance-attributes, invalid-name

"""metadata module"""

from dataclasses import dataclass
import json


@dataclass
class Dataset():
    '''Class for dataset objects'''

    dataset_id: str = None
    alias: str = None
    workspace_id: str = None
    title: str = None
    description: str = None
    questions: str = None
    raw_data: str = None
    visualisation: str = None
    metadata: str = None
    query: str = None

    def to_json(self):
        '''Converts the dataset class structure to a JSON string'''

        dict_repr = {}

        dict_repr.update({'id': self.dataset_id})
        dict_repr.update({'alias': self.alias})
        dict_repr.update({'workspaceId': self.workspace_id})
        dict_repr.update({'title': self.title})
        dict_repr.update({'description': self.description})
        dict_repr.update({'questions': self.questions})
        dict_repr.update({'rawData': self.raw_data})
        dict_repr.update({'visualisation': self.visualisation})
        dict_repr.update({'metadata': self.metadata})
        dict_repr.update({'query': self.query})

        filtered = {k: v for k, v in dict_repr.items() if v is not None}

        return json.dumps(filtered)

    @staticmethod
    def from_dict(datasets_dict):
        '''Resolves dataset(s) from a dictionary'''

        dataset = Dataset()

        dataset.dataset_id = datasets_dict.get('id')
        dataset.alias = datasets_dict.get('alias')
        dataset.workspace_id = datasets_dict.get('workspaceId')
        dataset.title = datasets_dict.get('title')
        dataset.description = datasets_dict.get('description')
        dataset.questions = datasets_dict.get('questions')
        dataset.raw_data = datasets_dict.get('rawData')
        dataset.visualisation = datasets_dict.get('visualisation')
        dataset.metadata = datasets_dict.get('metadata')
        dataset.query = datasets_dict.get('query')

        return dataset
