import httpx
from flask import current_app


class TemBoard(object):
    def __init__(self, url, verify=False):
        self.url = url
        self.client = httpx.Client(base_url=self.url, verify=verify)
        self.xsession = None

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, *a):
        self.client.__exit__(*a)
        self.client = None

    def __repr__(self):
        return '<%s %s %sconnected>' % (
            self.__class__.__name__,
            self.url,
            '' if self.client else 'dis',
        )

    def __getattr__(self, name):
        return getattr(self.client, name)

    def login(self, username=None, password=None):
        if not username:
            username, password = temboard_credentials()

        r = self.client.post(
            "/login",
            data=dict(username=username, password=password)
        )
        r.raise_for_status()
        return r

    def delete_instance(self, address, port):
        r = self.client.post(
            "/json/settings/delete/instance",
            json=dict(agent_address=address, agent_port=port)
        )
        r.raise_for_status()
        return r


def temboard_credentials():
    return current_app.config['TEMBOARD_CREDENTIALS'].split(':', 1)
