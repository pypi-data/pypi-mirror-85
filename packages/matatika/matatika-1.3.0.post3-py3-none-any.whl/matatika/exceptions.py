'''exceptions module'''

import textwrap


class MatatikaException(Exception):
    """Class to handle custom Matatika exceptions"""

    def __init__(self, message=None):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ContextNotSetError(Exception):
    """Class to raise an exception when a config context is not set"""

    def __init__(self, context, set_local_scope, set_global_scope):
        super().__init__()
        self.context = context
        self.set_local_scope = set_local_scope
        self.set_global_scope = set_global_scope

    def __str__(self):

        message = f"""{self.context[0].upper() + self.context[1:]} context not set\n
        You can provide {self.context} context scoped to a single command with 
        the '{self.set_local_scope}' option, or set a command-wide default using 
        '{self.set_global_scope}' (see '{self.set_global_scope} --help')"""

        return textwrap.dedent(message)


class WorkspaceContextNotSetError(ContextNotSetError):
    """Class to raise an exception when workspace context is not set"""

    def __init__(self):
        super().__init__("workspace", "--workspace / -w", "matatika use")


class EndpointURLContextNotSetError(ContextNotSetError):
    """Class to raise an exception when endpoint URL context is not set"""

    def __init__(self):
        super().__init__("endpoint URL", "--endpoint-url / -e", "matatika login")


class AuthContextNotSetError(ContextNotSetError):
    """Class to raise an exception when authentication token context is not set"""

    def __init__(self):
        super().__init__("authentication token", "--auth-token / -a", "matatika login")


class WorkspaceNotFoundError(Exception):
    """Class to raise an exception when a workspace is not found"""

    def __init__(self, endpoint_url, workspace_id):
        super().__init__()
        self.endpoint_url = endpoint_url
        self.workspace_id = workspace_id

    def __str__(self):
        message = f"Workspace {self.workspace_id} does not exist within the current authorisation" \
            f" context: {self.endpoint_url}"
        return textwrap.dedent(message)


class DatasetNotFoundError(Exception):
    """Class to raise an exception when a dataset is not found"""

    def __init__(self, dataset_id, endpoint_url):
        super().__init__()
        self.dataset_id = dataset_id
        self.endpoint_url = endpoint_url

    def __str__(self):
        message = f"Dataset {self.dataset_id} does not exist within the current authorisation" \
            f" context: {self.endpoint_url}"
        return textwrap.dedent(message)
