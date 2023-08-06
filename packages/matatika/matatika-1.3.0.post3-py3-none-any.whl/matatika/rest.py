"""rest module"""

import requests

class Client():
    """Class to handle client-side HTTP requests to the Matatika API"""

    def __init__(self, auth_token, endpoint_url, workspace_id=''):
        self.headers = {'content-type': 'application/json',
                        'Authorization': auth_token}

        self.datasets_url = '{}/workspaces/{}/datasets'.format(endpoint_url, workspace_id)
        self.workspace_url = '{}/workspaces'.format(endpoint_url)

    def get(self, url):
        """Makes a GET request"""

        return requests.get(url, headers=self.headers)

    def post(self, data):
        """Makes a POST request"""

        return requests.post(self.datasets_url, data=data, headers=self.headers)

    def get_workspace(self):
        """Returns all workspaces the user profile is a member of"""

        response = self.get(self.workspace_url)

        if response.status_code != 200:
            response.raise_for_status()

        data = response.json()
        workspaces = data['_embedded']['workspaces']

        return workspaces
