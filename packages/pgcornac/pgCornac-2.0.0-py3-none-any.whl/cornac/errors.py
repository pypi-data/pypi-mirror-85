import os


class KnownError(Exception):
    def __init__(self, message, exit_code=os.EX_SOFTWARE):
        super(KnownError, self).__init__(message)
        self.exit_code = exit_code


class RemoteCommandError(Exception):
    def __init__(self, message, exit_code, stderr):
        super().__init__(message)
        self.exit_code = exit_code
        self.stderr = stderr

    @property
    def connection_closed_by_remote(self):
        return (
            self.exit_code == 255 and
            'closed by remote host' in self.stderr)


class Timeout(Exception):
    pass
