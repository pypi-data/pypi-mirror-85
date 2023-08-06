# -*- coding: utf-8 -*-
"""rackio_modbus/api.py

This module implements a base class for retrieving tag mappings
"""
import json

from rackio.api import RackioResource

class MappingResource(RackioResource):

    def __init__(self, mapping):

        self.mapping = mapping

    def on_get(self, req, resp):

        resp.body = json.dumps(self.mapping, ensure_ascii=False)