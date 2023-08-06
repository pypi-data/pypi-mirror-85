'''
library module
'''

import json
from typing import List, Union

from requests.models import Response
from matatika.catalog import Catalog


class MatatikaClient():
    """
    Class to handle client context

    Args:
        auth_token (str): Authentication token
        endpoint_url (str): Endpoint URL
        workspace_id (str): Workspace ID

    Example:

    ```py
    # create 'auth_token', 'endpoint_url' and 'workspace-id' variables

    client = Matatika(auth_token, endpoint_url, workspace_id)
    ```
    """

    def __init__(self, auth_token, endpoint_url, workspace_id):
        self._auth_token = auth_token
        self._endpoint_url = endpoint_url
        self._workspace_id = workspace_id

    # getter methods
    @property
    def auth_token(self):
        """
        Gets the client auth token

        Returns:
            str: Client auth token

        Example:

        ```py
        # create MatatikaClient object

        auth_token = client.auth_token
        ```
        """

        return self._auth_token

    @property
    def endpoint_url(self):
        """
        Gets the client endpoint URL

        Returns:
            str: Client endpoint URL

        Example:

        ```py
        # create MatatikaClient object

        endpoint_url = client.endpoint_url
        ```
        """

        return self._endpoint_url

    @property
    def workspace_id(self):
        """
        Gets the client workspace URL

        Returns:
            str: Client workspace URL

        Example:

        ```py
        # create MatatikaClient object

        workspace_id = client.workspace_id
        ```
        """

        return self._workspace_id

    # setter methods
    @auth_token.setter
    def auth_token(self, value):
        """
        Sets the client authentication token

        Args:
            value (str): Authentication token

        Example:

        ```py
        # create MatatikaClient object
        # create 'auth_token' variable

        client.auth_token = auth_token
        ```
        """

        self._auth_token = value

    @endpoint_url.setter
    def endpoint_url(self, value):
        """
        Sets the client endpoint URL

        Args:
            value (str): Endpoint URL

        Example:

        ```py
        # create MatatikaClient object
        # create 'endpoint_url' variable

        client.endpoint_url = endpoint_url
        ```
        """

        self._endpoint_url = value

    @workspace_id.setter
    def workspace_id(self, value):
        """
        Sets the client workspace ID

        Args:
            value (str): Workspace ID

        Example:

        ```py
        # create MatatikaClient object
        # create 'workspace_id' variable

        client.workspace_id = workspace_id
        ```
        """

        self._workspace_id = value

    def profile(self) -> dict:
        """
        Gets the authenticated user profile

        Returns:
            dict: Authenticated user profile

        Example:

        ```py
        # create MatatikaClient object

        profile = client.profile()

        print(profile['id'])
        print(profile['name'])
        print(profile['email'])
        ```
        """

        catalog = Catalog(self)
        return catalog.get_profile()

    def publish(self, datasets: dict) -> List[Response]:
        """
        Publishes one or more datasets

        Args:
            datasets (dict): Datasets to publish

        Returns:
            List[Response]: Dataset publish responses

        ```py
        # create MatatikaClient object
        # create 'datasets' variable

        responses = client.publish(datasets)

        for response in responses:
            status_code = response.status_code

            if status_code in [201, 200]:
                dataset = response.json()
                msg = f"Successfully published the dataset '{dataset['alias']}'"
            else:
                alias = response.request.body['alias']
                msg = f"There was an eror publishing the dataset '{alias}'"

            print(f"{status_code} | {msg}")
        ```
        """

        catalog = Catalog(self)
        return catalog.post_datasets(datasets)

    def list_resources(self, resource_type: str) -> Union[list, None]:
        """
        Lists all available resources of the specified type

        Args:
            resource_type (str): Resource type to return (workspaces/datasets)

        Returns:
            Union[list,None]: Available resources

        Examples:

        List all workspaces
        ```py
        # create MatatikaClient object

        workspaces = client.list_resources('workspaces')

        for workspace in workspaces:
            print(" | ".join([workspace['id'], workspace['name']. dataset['domains']]))
        ```

        List all datasets in the workspace provided upon client object instantiation
        ```py
        # create MatatikaClient object

        datasets = client.list_resources('datasets')

        for dataset in datasets:
            print(" | ".join([dataset['id'], dataset['alias']. dataset['title']]))
        ```

        List all datasets in the workspace 'c6db37fd-df5e-4ac6-8824-a4608932bda0'
        ```py
        # create MatatikaClient object

        client.workspace_id = 'c6db37fd-df5e-4ac6-8824-a4608932bda0'
        datasets = client.list_resources('datasets')

        for dataset in datasets:
            print(" | ".join([dataset['id'], dataset['alias']. dataset['title']]))
        ```
        """

        catalog = Catalog(self)

        if resource_type == 'workspaces':
            return catalog.get_workspaces()

        if resource_type == 'datasets':
            return catalog.get_datasets()

        return None

    def fetch(self, dataset_id, raw=False) -> Union[dict, str]:
        """
        Fetches the data of a dataset using the query property

        Args:
            dataset_id (str): Dataset ID in UUID format
            raw (bool, optional): Whether to return the data as a raw string or not
            (defaults to False)

        Returns:
            Union[dict,str]: Dataset data

        Examples:

        Fetch data as Python object
        ```py
        # create MatatikaClient object
        # create 'dataset_id' variable

        data = dataset.fetch(dataset_id)

        if data not None:
            print(data)
        else:
            print(f"No data was found for dataset {dataset_id}")
        ```

        Fetch data as a raw string
        ```py
        # create MatatikaClient object
        # create 'dataset_id' variable

        data = dataset.fetch(dataset_id, raw=True)

        if data not None:
            print(data)
        else:
            print(f"No data was found for dataset {dataset_id}")
        ```
        """

        catalog = Catalog(self)
        data = catalog.get_data(dataset_id)

        if raw:
            return data

        return json.loads(data)
