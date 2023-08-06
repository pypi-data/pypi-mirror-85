from __future__ import print_function
import sys
import os
import requests
import logging
import json
from os.path import dirname
from jsonschema import validate
import importlib
import pkgutil
from halocli.util import Util

logger = logging.getLogger(__name__)

logging.root.setLevel(logging.INFO)


class PluginError(Exception):
    pass


class Plugin():

    def __init__(self, halo):
        # init vars
        self.halo = halo

        # init work on halo config
        # if self.halo.config ...

        self.name = 'setup'
        self.desc = 'config settings file'

        # set commands
        self.commands = {
            'config': {
                'usage': "Configure project settings file",
                'lifecycleEvents': ['config'],
                'options': {
                    'service_name': {
                        'usage': 'Name of service',
                        'required': True,
                        'shortcut': 's'
                    },
                    'swagger_path': {
                        'usage': 'Path to swagger file',
                        'required': True,
                        'shortcut': 'p'
                    }
                },
            },
        }

        # set hooks
        self.hooks = {
            'before:setup:config': self.before_setup_config,
            'setup:config': self.setup_config,
            'after:setup:config': self.after_setup_config,
        }

        # logger.info('finished plugin')

    def run_plugin(self, options):
        self.options = options
        # do more

    def before_setup_config(self):
        pass

    def setup_config(self):
        if hasattr(self, 'options'):
            for o in self.options:
                if 'service_name' in o:
                    service_name = o['service_name']
                if 'service_name' in o:
                    swagger_path = o['swagger_path']
        else:
            return
        ret = Util.config_settings(self.halo.settings, service_name,swagger_path)
        if ret == 0:
            self.halo.cli.log("finished config seccessfuly")
        return ret

    def after_setup_config(self):
        pass
