from __future__ import print_function
import sys
import os
import pip
import requests
import logging
import json
from os.path import dirname
from jsonschema import validate
import importlib
import pkgutil
import inspect
from .exception import ConfigException, ValidException, CliException, HaloPluginException
from swagger_py_codegen.command import spec_load, dump_file as dump_file_yml
import flex
from flex.exceptions import ValidationError

logger = logging.getLogger(__name__)


class Util():

    @staticmethod
    def check_new_version_available(this_version):
        """
        Checks if a newer version of Zappa is available.
        Returns True is updateable, else False.
        """


        pypi_url = 'https://pypi.python.org/pypi/Halo/json'
        resp = requests.get(pypi_url, timeout=1.5)
        top_version = resp.json()['info']['version']

        if this_version != top_version:
            return True
        else:
            return False

    @staticmethod
    def upper_first_letter(name):
        if name:
            if len(name.strip()) > 0:
                return name.strip().lower().title()
        return name

    @staticmethod
    def load_json_schema(filename,dir=None):
        """ Loads the given schema file """
        if dir is None:
            dir = dirname(__file__)
        absolute_path = os.path.join(dir, 'schemas', filename)

        base_path = dirname(absolute_path)
        base_uri = 'file://{}/'.format(base_path)

        with open(absolute_path) as schema_file:
            return json.loads(schema_file.read())

    @staticmethod
    def assert_valid_schema(data, schema_file,dir=None):
        """ Checks whether the given data matches the schema """

        schema = Util.load_json_schema(schema_file,dir)
        return validate(data, schema)

    @staticmethod
    def load_settings_file(settings_file=None):
        """
        Load our settings file.
        """
        logger.debug ("settings_file:"+str(settings_file))

        if not settings_file:
            settings_file = "halo_settings.json"
        if not os.path.isfile(settings_file):
            raise ConfigException("halo_settings file not found!.")

        with open(settings_file) as json_file:
            try:
                halo_settings = json.load(json_file)
            except ValueError as e:
                raise ConfigException("Unable to load the Halo settings JSON. It may be malformed. "+str(e))

        schema_file = "halo_schema.json"
        try:
            validated = Util.assert_valid_schema(halo_settings, schema_file)
            logger.debug("ret="+str(validated))
            #if not validated:
            #    raise ValidException("Please configure your halo_settings file properly!.")
        except Exception as e:
            raise ValidException("Please configure your halo_settings file properly:"+str(e))
        return halo_settings

    @staticmethod
    def check_package_in_env(name):
        package_name = name#.replace("-","_")
        if "./" in package_name:
            package_name = package_name.replace("./","")
        listx = []
        members = [name for _, name, _ in pkgutil.iter_modules([package_name])]
        if len(members) == 0:
            raise HaloPluginException("plugin package: " + package_name+" not installed")
        if len(members) > 0:
            members.remove("setup")
        for member in members:
            spec = importlib.util.find_spec(member,package_name)
            if not spec:
                raise HaloPluginException("plugin package: " + package_name + " not installed")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for namex, cls in inspect.getmembers(module, inspect.isclass):
                logger.debug("name:" + str(namex))
                methods = dir(cls)
                if  "run_plugin" in methods:
                    clazz = "{0}.{1}".format(cls.__module__, cls.__name__)
                    listx.append(clazz)
            logger.debug("listx:"+str(listx))
        return listx

    @staticmethod
    def install_plugin(package):
        import subprocess
        if "/" in package:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', "-e",package])
        else:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install',package])
        return 0

    @staticmethod
    def install_plugin1(package):
        if "/" in package:
            arg = "-e"
            if hasattr(pip, 'main'):
                z = pip.main(['install', arg, package])
            else:
                z = pip._internal.main(['install', arg, package])
            return z
        else:
            if hasattr(pip, 'main'):
                z = pip.main(['install', package])
            else:
                z = pip._internal.main(['install', package])
        return  z

    @staticmethod
    def dump_file(filename, data):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    @staticmethod
    def config_settings(service_name,swagger_path):
        pass

    ######
    @staticmethod
    def analyze_swagger(swagger_file_path):
        if not os.path.exists(swagger_file_path):
            raise ValidException("no such file:"+str(swagger_file_path))
        try:
            data = spec_load(swagger_file_path)
            return data
        except TypeError as e:
            raise ValidException(str(e))

    @staticmethod
    def validate_swagger(swagger_file):
        try:
            flex.core.parse(swagger_file)
            logging.debug("Swagger Validation passed")
            return True
        except ValidationError as e:
            raise ValidException(str(e))

    #####


class ImmutableDict(dict):
    def __setitem__(self, key, value):
        raise TypeError("%r object does not support item assignment" % type(self).__name__)

    def __delitem__(self, key):
        raise TypeError("%r object does not support item deletion" % type(self).__name__)

    def __getattribute__(self, attribute):
        if attribute in ('clear', 'update', 'pop', 'popitem', 'setdefault'):
            raise AttributeError("%r object has no attribute %r" % (type(self).__name__, attribute))
        return dict.__getattribute__(self, attribute)

    def __hash__(self):
        return hash(tuple(sorted(self.iteritems())))

    def fromkeys(self, S, v):
        return type(self)(dict(self).fromkeys(S, v))