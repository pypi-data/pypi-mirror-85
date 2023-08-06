'''CLI login test module'''

from unittest.mock import patch
from matatika.cli import matatika
from tests.test_cli import TestCLI


class TestCLILogin(TestCLI):
    '''Test class for CLI login command'''

    def test_login_without_required_opts(self):
        '''Test login without required options'''

        result = self.runner.invoke(matatika, ["login"])
        self.assertIn("Error: Missing option '--auth-token' / '-a'",
                      result.output)
        self.assertIs(result.exit_code, 2)

    def test_login_with_empty_required_opts(self):
        '''Test login with required options set to nothing'''

        # auth token
        result = self.runner.invoke(matatika, ["login",
                                               "-a"])
        self.assertIn("Error: -a option requires an argument",
                      result.output)
        self.assertIs(result.exit_code, 2)

    def test_login_with_invalid_auth_token(self):
        '''Test login with invalid auth token'''

        result = self.runner.invoke(matatika, ["login",
                                               "-a", "invalid-value"])
        self.assertIn("Please check your authentication token is correct and valid",
                      result.output)

    @patch('catalog.requests.get')
    @patch('catalog.jwt.decode', return_value=TestCLI.MOCK_DECODED_JWT)
    def test_login(self, _mock_decoded_jwt, mock_get_request):
        '''Test login'''

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = TestCLI.MOCK_PROFILE_RESPONSE

        result = self.runner.invoke(matatika, ["login",
                                               "-a", "auth-token"])
        self.assertIn("Successfully logged in",
                      result.output)
        self.assertIn(
            TestCLI.MOCK_PROFILE_RESPONSE['id'], result.output)
        self.assertIn(
            TestCLI.MOCK_PROFILE_RESPONSE['name'], result.output)

        self.assertIs(result.exit_code, 0)
