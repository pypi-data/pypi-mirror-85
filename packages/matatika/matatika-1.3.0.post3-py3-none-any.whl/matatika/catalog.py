"""catalog module"""

import jwt
import requests
from matatika.dataset import Dataset
from matatika.exceptions import DatasetNotFoundError
from matatika.exceptions import WorkspaceNotFoundError
from matatika.exceptions import MatatikaException


class Catalog:
    """Class to handle authorisation with the Matatika API"""

    def __init__(self, client):
        self.headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + client.auth_token
        }

        auth_token_payload = jwt.decode(
            client.auth_token, algorithms='RS256', verify=False)

        self.endpoint_url = client.endpoint_url
        self.profile_url = f'{self.endpoint_url}/profiles/{auth_token_payload["sub"]}'
        self.workspaces_url = f'{self.endpoint_url}/workspaces'

        if client.workspace_id:
            self.workspace_id = str(client.workspace_id)
            self.datasets_url = f'{self.endpoint_url}/workspaces/{self.workspace_id}/datasets'

    def post_datasets(self, datasets):
        """Publishes a dataset into a workspace"""

        publish_responses = []

        for alias in datasets:
            dataset = Dataset.from_dict(datasets[alias])
            dataset_json = dataset.to_json()

            response = requests.post(
                self.datasets_url, headers=self.headers, data=dataset_json)

            if response.status_code == 404:
                raise WorkspaceNotFoundError(
                    self.endpoint_url, self.workspace_id)

            if response.status_code not in [201, 200]:
                raise MatatikaException("An unexpected error occurred while publishing dataset [%s]"
                                        % response.status_code)

            publish_responses.append(response)

        return publish_responses

    def get_workspaces(self):
        """Returns all workspaces the user profile is a member of"""

        response = requests.get(self.workspaces_url, headers=self.headers)
        if response.status_code not in [200]:
            raise MatatikaException("An unexpected error occurred while fetching workspaces"
                                    "[{}] [{}]".format(response.status_code, self.workspaces_url))
        json_data = response.json()
        workspaces = json_data['_embedded']['workspaces']

        return workspaces

    def get_datasets(self):
        """Returns all datasets in the supplied workspace"""

        response = requests.get(self.datasets_url, headers=self.headers)
        if response.status_code != 200:
            raise MatatikaException("An unexpected error occurred while fetching datasets"
                                    f"[{response.status_code}] [{response.url}]")

        json_data = response.json()
        datasets = json_data['_embedded']['datasets']

        return datasets

    def get_profile(self):
        """Returns the user profile"""

        response = requests.get(self.profile_url, headers=self.headers)

        if response.status_code != 200:
            response.raise_for_status()

        return response.json()

    def get_data(self, dataset_id):
        '''Returns the data from a dataset'''

        url = f'{self.endpoint_url}/datasets/{dataset_id}/data'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 404:
            raise DatasetNotFoundError(dataset_id, self.endpoint_url)
        if response.status_code != 200:
            response.raise_for_status()

        return response.text
