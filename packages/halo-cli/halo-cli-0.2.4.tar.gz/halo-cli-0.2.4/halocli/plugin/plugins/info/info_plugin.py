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

        self.name = 'info'
        self.desc = 'Create new bian service'

        # set commands
        self.commands = {
            'details': {
                'usage': "Create new bian service project",
                'lifecycleEvents': ['create'],
                'options': {
                    'template': {
                        'usage': 'Template for the service',
                        'shortcut': 't'
                    },
                    'template_url': {
                        'usage': 'Template URL for the service. Supports: GitHub, BitBucket',
                        'shortcut': 'u'
                    },
                    'path': {
                        'usage': 'The path where the service should be created (e.g. --path my-service)',
                        'shortcut': 'p',
                    },
                    'name': {
                        'usage': 'Name for the service. Overwrites the default name of the created service.',
                        'shortcut': 'n',
                    },
                },
            },
        }

        # set hooks
        self.hooks = {
            'details:create': self.details_create,
        }

        # logger.info('finished plugin')

    def run_plugin(self, options):
        self.options = options
        # do more


    def details_create(self):
        if hasattr(self, 'options'):
            for o in self.options:
                if 'template' in o:
                    template = o['template']
                if 'template_url' in o:
                    template_url = o['template_url']
                if 'path' in o:
                    path = o['path']
                if 'name' in o:
                    name = o['name']
        else:
            return
        #ret = Util.config_settings(self.halo.settings, template,template_url,path,name)
        #if ret == 0:
        #    self.halo.cli.log("finished config seccessfuly")
        ret = 3
        return ret


