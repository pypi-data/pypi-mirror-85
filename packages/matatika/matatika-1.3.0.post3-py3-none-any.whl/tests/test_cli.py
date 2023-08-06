'''CLI test module'''

import unittest
from unittest.mock import Mock
from unittest.mock import patch
from click.testing import CliRunner
from matatika.config import MatatikaConfig


class TestCLI(unittest.TestCase):
    '''Test class for CLI'''

    UNUSED_UUID = '9adc6c98-56c5-4934-8d1e-12696cd11bab'

    MOCK_DECODED_JWT = {
        'sub': 'provider|profile-id'
    }

    MOCK_PROFILE_RESPONSE = {
        'id': MOCK_DECODED_JWT['sub'],
        'name': 'profile name'
    }

    MOCK_WORKSPACES = [
        '89969253-723d-415d-b199-bcac2aaa4cde',
        '9f47ec52-41da-46eb-be7e-f7ef65490081'
    ]

    MOCK_WORKSPACES_RESPONSE = {
        '_embedded': {
            'workspaces': [
                {
                    'id': MOCK_WORKSPACES[0],
                    'name': 'workspace 1'
                },
                {
                    'id': MOCK_WORKSPACES[1],
                    'name': 'workspace 2'
                }
            ]
        }
    }

    MOCK_DATASETS = [
        '280a2ab2-f30e-4200-b765-ed73af3d63db',
        'c50d444f-a71d-4f29-a2cc-ee905ddc1e15'
    ]

    MOCK_DATASETS_RESPONSE = {
        '_embedded': {
            'datasets': [
                {
                    'id': MOCK_DATASETS[0],
                    'alias': 'dataset-1',
                    'title': 'dataset 1'
                },
                {
                    'id': MOCK_DATASETS[1],
                    'alias': 'dataset-2',
                    'title': 'dataset 2'
                }
            ]
        }
    }

    MOCK_DATA = {
        "google_analytics_active_user_stats.total_daily_active_users": 9,
        "google_analytics_active_user_stats.total_weekly_active_users": 26,
        "google_analytics_active_user_stats.total_14d_active_users": 75,
        "google_analytics_active_user_stats.total_28d_active_users": 201,
    }

    config = MatatikaConfig()

    def setUp(self):

        # overide config file read and write methods

        patcher = patch('cli.MatatikaConfig.get_default_workspace',
                        return_value='default-workspace')
        self.addCleanup(patcher.stop)
        self.mock_get_default_workspace = patcher.start()

        patcher = patch('cli.MatatikaConfig.set_default_workspace', Mock())
        self.addCleanup(patcher.stop)
        patcher.start()

        patcher = patch('cli.MatatikaConfig.get_endpoint_url',
                        return_value='endpoint-url')
        self.addCleanup(patcher.stop)
        self.mock_get_endpoint_url = patcher.start()

        patcher = patch('cli.MatatikaConfig.set_endpoint_url', Mock())
        self.addCleanup(patcher.stop)
        patcher.start()

        patcher = patch('cli.MatatikaConfig.get_auth_token',
                        return_value='auth-token')
        self.addCleanup(patcher.stop)
        self.mock_get_auth_token = patcher.start()

        patcher = patch('cli.MatatikaConfig.set_auth_token', Mock())
        self.addCleanup(patcher.stop)
        patcher.start()

        # instantiate a cli runner
        self.runner = CliRunner()
