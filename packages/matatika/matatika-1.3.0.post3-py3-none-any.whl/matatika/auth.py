"""auth module"""

from os import environ as env
import http.client
import json

from dotenv import load_dotenv, find_dotenv


class MatatikaAuth:
    """Class to handle authorisation with the Matatika API"""

    def __init__(self):
        env_file = find_dotenv()
        if env_file:
            load_dotenv(env_file)
        self.auth_domain = env.get("AUTH0_DOMAIN")
        self.audience = env.get("API_IDENTIFIER")
        self.client_id = env.get("CLIENT_ID")
        self.client_secret = env.get("CLIENT_SECRET")
        self.grant_type = env.get("GRANT_TYPE")
        self.algo = ["RS256"]

    @staticmethod
    def get_endpoint_url():
        """Returns the endpoint URL"""

        return env.get("ENDPOINT_URL")

    def get_auth_token(self):
        """Retrieves an auth token"""

        conn = http.client.HTTPSConnection(self.auth_domain)
        payload = {}
        payload['client_id'] = self.client_id
        payload['client_secret'] = self.client_secret
        payload['audience'] = self.audience
        payload['grant_type'] = self.grant_type

        headers = {'content-type': "application/json"}

        conn.request("POST", "/oauth/token", json.dumps(payload), headers)

        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))
        auth_token = ("%s %s" %
                      (json_data['token_type'], json_data['access_token']))

        return auth_token
