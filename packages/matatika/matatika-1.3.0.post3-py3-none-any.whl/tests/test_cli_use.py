'''CLI use test module'''

from unittest.mock import patch
from matatika.cli import matatika
from tests.test_cli import TestCLI


class TestCLIUse(TestCLI):
    '''Test class for CLI use command'''

    def test_use_with_invalid_workspace_id_opt(self):
        '''Test use with invalid workspace id option'''

        result = self.runner.invoke(matatika, ["use",
                                               "-w", "invalid-value"])
        self.assertIn("Invalid value for '--workspace-id' / '-w': invalid-value is not a valid "
                      "UUID value", result.output)

    @patch('catalog.requests.get')
    @patch('catalog.jwt.decode', return_value=TestCLI.MOCK_DECODED_JWT)
    def test_use_with_workspace_id_not_found_in_auth_context(self, _mock_decoded_jwt,
                                                             mock_get_request):
        '''Test use with workspace ID not found in the authentication context'''

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.text = str(TestCLI.MOCK_WORKSPACES)

        workspace_id = TestCLI.UNUSED_UUID

        result = self.runner.invoke(matatika, ["use",
                                               "-w", workspace_id])
        self.assertIn(f"Workspace {workspace_id} does not exist within the current authorisation "
                      f"context: {self.mock_get_endpoint_url.return_value}", result.output)

    def test_use_with_no_opts(self):
        '''Test use with no options'''

        result = self.runner.invoke(matatika, ["use"])
        self.assertIn(f"Workspace context set to {self.mock_get_default_workspace.return_value}",
                      result.output)

    @patch('catalog.requests.get')
    @patch('catalog.jwt.decode', return_value=TestCLI.MOCK_DECODED_JWT)
    @patch('cli.MatatikaConfig.get_default_workspace', return_value='test-workspace')
    def test_use_with_workspace_id_opt(self, mock_get_default_workspace, _mock_decoded_jwt,
                                       mock_get_request):
        '''Test use with workspace ID option'''

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = TestCLI.MOCK_WORKSPACES_RESPONSE

        workspace_id = TestCLI.MOCK_WORKSPACES[0]

        result = self.runner.invoke(matatika, ["use",
                                               "-w", workspace_id])
        self.assertIn(f"Workspace context set to {mock_get_default_workspace.return_value}",
                      result.output)
