import logging
from urllib.parse import urlparse

import httpx
from flask import current_app
from etcd import Client as EtcdClient, EtcdKeyNotFound

from .errors import KnownError


__all__ = ['EtcdKeyNotFound']


logger = logging.getLogger(__name__)


def connect():
    username, password = etcd_credentials()
    for url_string in current_app.config['ETCD']:
        url = urlparse(url_string)
        try:
            return ClientManager(
                protocol=url.scheme, host=url.hostname, port=url.port or 2379,
                username=username, password=password,
            )
        except Exception as e:
            logger.debug("Failed to connect to etcd %s: %s", url_string, e)
    else:
        raise KnownError("Failed to connect to any etcd host.")


def etcd_credentials():
    return current_app.config['ETCD_CREDENTIALS'].split(':', 1)


class Client(EtcdClient):
    def http_delete(self, path):
        url = f'{self.protocol}://{self.host}:{self.port}/v2'
        auth = (self.username, self.password)
        return httpx.delete(url + path, auth=auth)

    def http_get(self, path):
        url = f'{self.protocol}://{self.host}:{self.port}/v2'
        auth = (self.username, self.password)
        return httpx.get(url + path, auth=auth)


class ClientManager(object):
    def __init__(self, **kw):
        self.kw = kw
        self.client = None

    def __enter__(self) -> Client:
        self.client = Client(**self.kw)
        return self.client

    def __exit__(self, *_):
        del self.client
