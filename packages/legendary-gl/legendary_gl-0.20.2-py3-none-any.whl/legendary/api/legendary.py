# !/usr/bin/env python
# coding: utf-8

import requests
import logging

from legendary import __version__


class LegendaryAPI:
    _api_host = 'legendary.rodney.io'

    def __init__(self):
        self.log = logging.getLogger('LGDAPI')
        self.session = requests.session()
        self.session.headers['user-agent'] = f'Legendary/{__version__}'

    def get_version_info(self):
        r = self.session.get(f'https://{self._api_host}/version.json')
        r.raise_for_status()
        return r.json()
