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

        self.name = 'schema'
        self.desc = 'test settings file'

        # set commands
        self.commands = {
            'testx': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['resources', 'functions'],
                'options': {
                    'attribute': {
                        'usage': 'Name of the attribute',
                        'required': True,
                        'shortcut': 's'
                    },
                    'value': {
                        'usage': 'Value of the attribute',
                        'shortcut': 'v'
                    }
                },
            },
        }

        # set hooks
        self.hooks = {
            'before:valid:resources': self.before_valid_resources,
            'valid:resources': self.valid_resources,
            'after:valid:functions': self.after_valid_functions,
        }

        # logger.info('finished plugin')

    def run_plugin(self, options):
        self.options = options
        # do more

    def before_valid_resources(self):
        pass

    def valid_resources(self):
        if hasattr(self, 'options'):
            for o in self.options:
                if 'attribute' in o:
                    service = o['attribute']
        else:
            return
        ret = Util.valid(self.halo.settings, service)
        if ret == 0:
            self.halo.cli.log("finished valid seccessfuly")
        return ret

    def after_valid_functions(self):
        pass
