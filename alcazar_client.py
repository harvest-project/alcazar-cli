import base64
import urllib.parse

import requests


class AlcazarRemoteException(Exception):
    pass


class AlcazarClient:
    def __init__(self, host, port, token):
        self.host = host
        self.port = port
        self.token = token
        self.timeout = 30
        self._session = requests.Session()

    def _get_url(self, endpoint):
        return urllib.parse.urljoin('http://{}:{}'.format(self.host, self.port), endpoint)

    def _request(self, method, endpoint, *args, **kwargs):
        kwargs.setdefault('timeout', self.timeout)

        try:
            resp = self._session.request(method, self._get_url(endpoint), *args, **kwargs)
        except requests.exceptions.ConnectionError:
            raise AlcazarRemoteException('Error connecting to Alcazar. Please check if it is running and connectable.')

        return resp.json()

    def pop_updates(self):
        return self._request('POST', '/pop_updates')

    def ping(self):
        return self._request('GET', '/ping')

    def add_torrent(self, realm_name, torrent_file, download_path):
        return self._request('POST', '/torrents/{}'.format(realm_name), json={
            'torrent': base64.b64encode(torrent_file).decode(),
            'download_path': download_path,
        })

    def remove_torrent(self, realm_name, info_hash):
        return self._request('DELETE', '/torrents/{}/{}'.format(realm_name, info_hash))

    def get_config(self):
        return self._request('GET', '/config')

    def save_config(self, config):
        return self._request('PUT', '/config', json=config)

    def get_clients(self):
        return self._request('GET', '/clients')

    def add_client(self, client_data):
        return self._request('POST', '/clients', json=client_data)
