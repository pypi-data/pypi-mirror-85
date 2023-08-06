'''CLI list test module'''

from unittest.mock import patch
from matatika.cli import matatika
from tests.test_cli import TestCLI


class TestCLIList(TestCLI):
    '''Test class for CLI list command'''

    def test_list_no_subcommmand(self):
        '''Test list with no subcommand'''

        result = self.runner.invoke(matatika, ["list"])
        self.assertIn(
            "Usage: matatika list [OPTIONS] COMMAND [ARGS]...", result.output)
        self.assertIs(result.exit_code, 0)

    def test_list_invalid_subcommand(self):
        '''Test list with an invalid subcommand'''

        resource_type = "invalid-resource-type"

        result = self.runner.invoke(matatika, ["list", resource_type])
        self.assertIn(
            f"Error: No such command '{resource_type}'.", result.output)
        self.assertIs(result.exit_code, 2)

    @patch('catalog.requests.get')
    @patch('catalog.jwt.decode', return_value=TestCLI.MOCK_DECODED_JWT)
    @patch('cli.MatatikaConfig.get_endpoint_url', return_value='endpoint url')
    def test_list_workspaces(self, _mock_endpoint_url, _mock_decoded_jwt, mock_get_request):
        '''Test list workspaces'''

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = TestCLI.MOCK_WORKSPACES_RESPONSE

        result = self.runner.invoke(matatika, ["list", "workspaces"])
        for mock_workspace in TestCLI.MOCK_WORKSPACES:
            self.assertIn(mock_workspace, result.output)

        self.assertIn(f"Total workspaces: {len(TestCLI.MOCK_WORKSPACES)}",
                      result.output)

    @patch('catalog.requests.get')
    @patch('catalog.jwt.decode', return_value=TestCLI.MOCK_DECODED_JWT)
    @patch('cli.MatatikaConfig.get_endpoint_url', return_value='endpoint url')
    def test_list_datasets(self, _mock_endpoint_url, _mock_decoded_jwt, mock_get_request):
        '''Test list datasets'''

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = TestCLI.MOCK_DATASETS_RESPONSE

        result = self.runner.invoke(matatika, ["list",
                                               "datasets",
                                               "-w",
                                               TestCLI.MOCK_WORKSPACES[0]])
        for mock_workspace in TestCLI.MOCK_DATASETS:
            self.assertIn(mock_workspace, result.output)

        self.assertIn(f"Total datasets: {len(TestCLI.MOCK_DATASETS)}",
                      result.output)
