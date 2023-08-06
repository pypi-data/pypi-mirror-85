import os
import sys
import re
import time
import traceback
import click
import six
from rich.console import Console
from rich.table import Column, Table
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)
from pyfiglet import figlet_format

try:
    import colorama

    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

import halocli
from halocli.util import Util
from halocli.exception import CliException,ConfigException,HaloCommandException,HaloPluginMngrException
from halocli.plugin.plugin_manager import PluginMngr

class Cmd():

    def __init__(self,cli,plugin_mngr):
        self.cli = cli
        self.plugin_mngr = plugin_mngr

    def get_commands(self,plugin):
        commands = []
        plugin_commands = self.plugin_mngr.plugin_commands[plugin]
        for c in plugin_commands:
            name = c['name']
            options = None
            help = None
            sub_commands = None
            if 'options' in c['body']:
                options = c['body']['options']
            if 'usage' in c['body']:
                help = c['body']['usage']
            if 'commands' in c['body']:
                sub_commands = c['body']['commands']
            rec = {'name': name,'options': options,'help':help,'commands':sub_commands}
            commands.append(rec)
        return commands

    def bind_plugin_function(self,name, p):
        doc = ''
        if p.desc:
            doc = p.desc
        @click.group(name=p.name,short_help=doc)
        def funcg():
            pass

        return funcg,p.name

    def bind_command_function(self,name, c):
        options = {}
        if 'options' in c and c['options'] != None:
            options = c['options']
        @click.pass_context
        def func(ctx,**p):
            args = []
            for o in options:
                option_name = o
                if option_name in p:
                    option_value = p[option_name]
                args.append({option_name:option_value})
            try:
                self.plugin_mngr.run_command(ctx,c['name'],args)
            except Exception as e:
                if ctx.obj.debug:
                    stack = traceback.format_exc()
                    print(str(stack))
                self.cli.error("Error in HALO CLI Command : " + str(e))


        func.__name__ = name
        if 'help' in c:
            func.__doc__ = c['help']
        return func

    def create_command_groups(self,plugins,cli):
        list = {}
        for p in plugins:
            f,name = self.bind_plugin_function('_f', p)
            cli.add_command(f)
            self.create_commands_for_group(f,p)
            list[name] = f
        return list

    def create_commands_for_group(self,grp,p):
        for c in self.get_commands(p):
            f = self.bind_command_function('_f', c)
            _f = grp.command(name=c['name'])(f)
            self.add_option(_f,c)


    def add_option(self,f,c):
        if 'options' in c and c['options'] != None:
            options = c['options']
            for o in options:
                option_name = o
                option_usage = None
                option_shortcut = None
                option_default = None
                option_required = False
                if 'usage' in options[o]:
                    option_usage = options[o]['usage']
                if 'shortcut' in options[o]:
                    option_shortcut = options[o]['shortcut']
                if 'default' in options[o]:
                    option_default = options[o]['default']
                if 'required' in options[o]:
                    option_required = options[o]['required']
                opt_params = {
                    "name": option_name,
                    "short": option_shortcut,
                    "long": option_name,
                    "type": "string",
                    "help": option_usage,
                    "required": option_required,
                    "default": option_default
                }
                map_to_types = dict(
                    array=str,
                    number=float,
                    string=str,
                )
                param_decls = (
                    '-' + opt_params['short'],
                    '--' + opt_params['long'],
                    opt_params['name'])
                attrs = dict(
                    required=opt_params['required'],
                    help=opt_params['help'],
                    default=opt_params['default'],
                    type=map_to_types.get(
                        opt_params['type'], opt_params['type'])
                )
                click.option(*param_decls, **attrs)(f)




