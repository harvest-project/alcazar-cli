#!/usr/bin/env python3

import argparse
import json

from alcazar_client import AlcazarClient


def json_dumps(obj):
    return json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)


class AlcazarCLI:
    def __init__(self, host, port, token):
        self._client = AlcazarClient(host, port, token)

    def add_torrent(self, args):
        try:
            with open(args.torrent_path, 'rb') as f:
                torrent_data = f.read()
        except (OSError, IOError):
            raise Exception('Unable to read .torrent file.')

        torrent = self._client.add_torrent(args.realm, torrent_data, args.download_path)
        print('Torrent added: {}'.format(torrent['name']))

    def remove_torrent(self, args):
        self._client.remove_torrent(args.realm, args.info_hash)
        print('Removed torrent.')

    def ping(self, args):
        self._client.ping()
        print('Ping is successful.')

    def get_config(self, args):
        config = self._client.get_config()
        print(json_dumps(config))

    def list_clients(self, args):
        clients = self._client.get_clients()
        print(json_dumps(clients))


def main():
    parser = argparse.ArgumentParser(description='Alcazar command line client.')
    parser.add_argument('--host', default='localhost', help='Host used to connect to the Alcazar instance.')
    parser.add_argument('-p', '--port', default=7001, help='Port used to connect to the Alcazar instance.')
    parser.add_argument('-t', '--token', default='', help='API token used to connect to the Alcazar instance.')

    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    subparsers.required = True

    subparsers.add_parser('ping')
    subparsers.add_parser('get-config')
    subparsers.add_parser('list-clients')

    parser_add_torrent = subparsers.add_parser('add-torrent')
    parser_add_torrent.add_argument('realm', help='Realm name to add the torrent to.')
    parser_add_torrent.add_argument('torrent_path', help='Path to the .torrent file.')
    parser_add_torrent.add_argument('download_path', help='Directory where to download the torrent.')

    parser_remove_torrent = subparsers.add_parser('remove-torrent')
    parser_remove_torrent.add_argument('realm', help='Realm name to remove the torrent from.')
    parser_remove_torrent.add_argument('info_hash', help='Info hash of the torrent to remove.')

    args = parser.parse_args()

    cli = AlcazarCLI(args.host, args.port, args.token)
    try:
        return getattr(cli, args.command.replace('-', '_'))(args) or 0
    except Exception as exc:
        print('Error running {}: {}'.format(args.command, exc))


if __name__ == '__main__':
    main()
