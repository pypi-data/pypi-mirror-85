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

    def __init__(self,halo):
        #init vars
        self.halo = halo

        #init work on halo config
        #if self.halo.config ...

        self.name = 'plugin'
        self.desc = 'install plugin'

        # set commands
        self.commands = {
            'install': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['resources'],
                'options': {
                    'name': {
                        'usage': 'Name of plugin',
                        'required': True,
                        'shortcut': 'n'
                    }
                },
            },
        }

        # set hooks
        self.hooks = {
            'install:resources': self.install_resources
        }

        #logger.info('finished plugin')

    def run_plugin(self,options):
        self.options = options


    def install_resources(self):
        p = None
        if hasattr(self, 'options'):
            if self.options:
                for o in self.options:
                    if 'name' in o:
                        p = o['name']
        if not p:
            raise Exception("no plugin found")
        if not self.is_plugin(p):
            raise Exception('plugin ' + p+' not a Halo plugin')
        ret = Util.install_plugin(p)
        if ret == 0:
            self.halo.cli.log("finished install seccessfuly")
        else:
            raise Exception('Installation failed for plugin '+p)

    def is_plugin(self,plugin):
        if plugin:
            return True



