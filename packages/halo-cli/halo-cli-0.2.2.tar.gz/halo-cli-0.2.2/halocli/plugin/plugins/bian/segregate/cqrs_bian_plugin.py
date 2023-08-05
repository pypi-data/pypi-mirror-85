from __future__ import print_function
import sys
import os
import logging
import json
import copy
from os.path import dirname
from jsonschema import validate
import importlib
import pkgutil
import tempfile
import uuid
from halocli.exception import HaloPluginException
from halocli.util import Util

logger = logging.getLogger(__name__)

logging.root.setLevel(logging.INFO)

"""
the bian plugin
---------------

1. extend with no segregation endpoints

2. add id for no segregation items

"""

class Plugin():

    def __init__(self,halo):
        #init vars
        self.halo = halo

        #init work on halo config
        #if self.halo.config ...

        self.name = 'cqrs'
        self.desc = 'ammend bian swagger file for no cqrs'

        # set commands
        self.commands = {
            'method': {
                'usage': "do this for your HALO project",
                'lifecycleEvents': ['generate', 'write'],
                'options': {
                    'service': {
                        'usage': 'Name of the service',
                        'shortcut': 's',
                        'required': True
                    },
                    'path': {
                        'usage': 'Path of the swagger file',
                        'shortcut': 'p',
                        'required': True
                    },
                    'id': {
                        'usage': 'add reference id to items',
                        'shortcut': 'i'
                    }
                },
            },
        }

        # set hooks
        self.hooks = {
            'before:method:generate': self.before_method_generate,
            'method:generate': self.method_generate,
            'after:method:generate': self.after_method_generate,
            'method:write': self.method_write,
        }

        #logger.info('finished plugin')

    def run_plugin(self,options):
        self.options = options
        #do more


    def before_method_generate(self):
        self.id = None
        for o in self.options:
            if 'service' in o:
                self.service = o['service']
            if 'path' in o:
                self.path = o['path']
            if 'id' in o:
                self.id = o['id']
        if self.service not in self.halo.settings['mservices']:
            raise HaloPluginException("service not found in swagger : "+self.service)
        urls = self.halo.settings['mservices'][self.service]['urls']
        self.data = Util.analyze_swagger(urls)


    def method_generate(self):
        data = self.data
        tmp = {}
        bqs = []
        for d in data['paths']:
            m = data['paths'][d]
            if 'get' in m:
                if d.endswith("/behavior-qualifiers/"):
                    logger.debug("bqs:" + str(m))
                    bqs = m['get']['responses']['200']['schema']['example']
                if m['get']['operationId'].endswith('ReferenceIds'):
                    logger.debug(str(m))
                    new_m = copy.deepcopy(m)
                    new_m['get']['operationId'] = m['get']['operationId'] + "Extend"
                    tmp[d] = new_m
        # fix the response and add
        for k in tmp:
            # bq methods
            if "{cr-reference-id}" in k:
                for item in bqs:
                    ref_key = k.replace("{behavior-qualifier}", item.lower()) + "{bq-reference-id}/"
                    ref_m = data['paths'][ref_key]
                    new_m = copy.deepcopy(ref_m)
                    props = new_m['get']['responses']['200']['schema']['properties']
                    key = k.replace("{behavior-qualifier}", item.lower()) + "extend"
                    m = tmp[k]
                    new_m = copy.deepcopy(m)
                    new_m['get']['responses']['200']['schema']['items']['type'] = 'object'
                    new_m['get']['responses']['200']['schema']['items']['properties'] = props
                    new_m['get']['responses']['200']['schema']['example'] = []
                    new_m['get']['operationId'] = new_m['get']['operationId'] + item
                    if self.id:
                        for p in props:
                            if p.endswith(self.id):
                                props[p]['properties']["ObjectReference"] = {"type": "string"}
                    params = new_m['get']['parameters']
                    for p in params:
                        if p['name'] == "behavior-qualifier":
                            params.remove(p)
                    new_m['get']['parameters'] = params
                    new_m['get']['summary'] = new_m['get']['summary'].replace("Reference Ids", 'Instances')
                    if 'description' in new_m['get']:
                        new_m['get']['description'] = new_m['get']['description'].replace("Reference Ids", 'Instances')
                    data['paths'][key] = new_m
            else:  # cr methods
                ref_key = k + "/{cr-reference-id}"
                ref_m = data['paths'][ref_key]
                new_m = copy.deepcopy(ref_m)
                props = new_m['get']['responses']['200']['schema']['properties']
                key = k + "/extend"
                m = tmp[k]
                m['get']['responses']['200']['schema']['items']['type'] = 'object'
                m['get']['responses']['200']['schema']['items']['properties'] = props
                m['get']['responses']['200']['schema']['example'] = []
                m['get']['summary'] = m['get']['summary'].replace("Ids", 'Instances')
                if 'description' in m['get']:
                    m['get']['description'] = m['get']['description'].replace("Ids", 'Instances')
                if self.id:
                    for p in props:
                        if p.endswith(self.id):
                            props[p]['properties']["ObjectReference"] = {"type": "string"}
                data['paths'][key] = m

        self.halo.cli.log("finished cqrs successfully")

    def after_method_generate(self):
        data = self.data
        Util.validate_swagger(data)

    def method_write(self):
        try:
            path = self.path
            if path:
                file_path = os.path.join(path, str(uuid.uuid4()) + ".json")
            else:
                dir_tmp = tempfile.TemporaryDirectory()
                file_path = os.path.join(dir_tmp.name, str(uuid.uuid4()) + ".json")
            logger.debug(file_path)
            f = open(file_path, "a")
            f.write("")
            f.close()
            Util.dump_file(file_path, self.data)
            logging.debug("Swagger file generated:" + file_path)
            """
            with open(file_path, 'r') as fi:
                f = fi.read()
                print(str(f))
                return f
            """
        except Exception as e:
            raise HaloPluginException(str(e))




