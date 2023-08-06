#system
import os
import sys
import logging
import re
import time
import importlib
import inspect
import pkgutil
#app
import click
import six
from pprint import pprint
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

from halocli.util import Util
from halocli.exception import CliException,ConfigException,HaloCommandException,HaloPluginMngrException,HaloPluginClassException
from halocli.plugin.plugin_manager import PluginMngr
from halocli.plugin.command import Cmd

logger = logging.getLogger(__name__)

console = Console()

#globals
builder = None

#log colors
verbose_clr = "yellow"
debug_clr = "blue"
verbose_clr = "green"

inquirer_style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules()
    if name.endswith('c')
}
#print("plugins:"+str(discovered_plugins))

def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)

def logx(plugins):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("plugin events", style="dim", width=60)
    table.add_column("Milliseconds")
    with click.progressbar(plugins) as click_plugins:
        for plugin in click_plugins:
            plugin_length = plugins[plugin]
            table.add_row(plugin, str(plugin_length))
    console.print(table)

def logy(argsx):
    from clint.arguments import Args
    from clint.textui import puts, colored as coloredx, indent
    args = Args()
    print()
    with indent(4, quote='>>>'):
        puts(coloredx.blue('Command Arguments: ') + str(argsx))
        puts(coloredx.blue('Arguments passed in: ') + str(args.all))
        puts(coloredx.blue('Flags detected: ') + str(args.flags))
        puts(coloredx.blue('Files detected: ') + str(args.files))
        puts(coloredx.blue('NOT Files detected: ') + str(args.not_files))
        puts(coloredx.blue('Grouped Arguments: ') + str(dict(args.grouped)))

    print()

def more(log_string):
    click.echo_via_pager(log_string)

def edit(msg):
    commit_message = click.edit()
    return  commit_message

def prompt_cli(msg, args):
    return click.prompt(msg,args)

def prompt_confirm():
    questions = [
        {
            'type': 'confirm',
            'message': 'Do you want to continue?',
            'name': 'continue',
            'default': True,
        },
        {
            'type': 'confirm',
            'message': 'Do you want to exit?',
            'name': 'exit',
            'default': False,
        },
    ]

    answers = prompt.prompt(questions, style=inquirer_style)
    pprint(answers)
    for item in answers:
        if item == 'continue':
            if not answers[item]:
                raise CliException(" not confirmed")

"""
UNIX

0 - success

1 - fail
----
If an ClickException is raised, invoke the ClickException.show() method on it to display it and then exit the program with ClickException.exit_code.

If an Abort exception is raised print the string Aborted! to standard error and exit the program with exit code 1.

if it goes through well, exit the program with exit code 0.
"""
def start(run=None,options=None):
    global builder
    log("HALO CLI", color="blue", figlet=True)
    log("Welcome to HALO CLI", "green")
    try:
        builder = Builder(options)
    except ConfigException as e:
        log("Error in HALO CLI Config: "+str(e), "red")
        sys.exit(1)
    except CliException as e:
        log("Error in HALO CLI: "+str(e), "red")
        sys.exit(1)
    except Exception as e:
        log("General Error in HALO CLI: "+str(e), "red")
        sys.exit(1)
    try:
        command_groups = builder.create_command_groups()
    except ConfigException as e:
        log("Error in HALO CLI Cmd Config: "+str(e), "red")
        sys.exit(1)
    except CliException as e:
        log("Error in HALO CLI Cmd: "+str(e), "red")
        sys.exit(1)
    except Exception as e:
        log("General Error in HALO CLI Cmd: "+str(e), "red")
        sys.exit(1)
    for cg_name in command_groups:
        cg = command_groups[cg_name]
        cli.add_command(cg,name=cg_name)
    """
        CLI for running halo commands
    """
    if run != False:
        try:
            return cli(auto_envvar_prefix='HALO')
        except SystemExit as e:
            if e.code != 0:
                log("\nError in HALO CLI Cmd: " + str(e.code), "red")
            sys.exit(1)

    return cli

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('-v','--version', is_flag=True,help='Print the Halo cli version')
@click.option('-a','--all', is_flag=True,help='Execute this command for all projects')
@click.option('-s','--settings_file', help='The path to a Halo settings file')
@click.option('-q','--quiet', is_flag=True,help='Silence all output')
@click.option('-r', '--verbose',is_flag=True,help='Verbose output')
@click.pass_context
def cli(ctx,debug,version,all,settings_file,quiet,verbose):
    """halocli - HALO framework cli tool"""
    #options
    if debug:
        logger.setLevel(logging.DEBUG)
        log('Debug mode is %s' % ('on' if debug else 'off'),"blue")
    if version:
        #log('Halo Version: {}'.format(halocli.__version__),"blue")
        log('Click Version: {}'.format(click.__version__),"blue")
        log('Python Version: {}'.format(sys.version),"blue")
    if verbose:
        log('Verbosity: %s' % verbose,"blue")
    if settings_file:
        log('settings file: {}'.format(settings_file), "blue")
    #context
    ctx.obj = Base(debug,all,quiet,verbose)
    #cfg dir
    app_dir = click.get_app_dir("halocli")
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    cfg = os.path.join(app_dir, "config")



class Base:

    def __init__(self,debug,all,quiet,verbose):
        self.debug = debug
        self.all = all
        self.quiet = quiet
        self.verbose = verbose

class Log:
    def error(self,msg):
        log(msg,"red")

    def log(self,msg):
        log(msg,"green")

class HaloProxy:

    cli = None
    variables = None
    settings = None

    def __init__(self,cli,variables,settings):
        self.cli = cli
        self.variables = variables
        self.settings = settings

class Builder:

    cli = Log()
    variables = {}
    settings = None
    names = {}
    proxy = None

    def __init__(self,options=None):
        if options:
            self.options = options
        else:
            self.options = sys.argv[1:]
        self.plugins = self.get_plugins()
        self.cmd = Cmd(self.cli,self.plugin_mngr)

    def logx(self,dict_run):
        logx(dict_run)

    def logy(self,args):
        logy(args)

    def get_plugins(self):
        halo_settings_path = None
        if self.options and "-s" in self.options:
            get = False
            for item in self.options:
                if item.strip() == "-s":
                    get = True
                    continue
                if get:
                    halo_settings_path = item
                    break
            if halo_settings_path:
                #@todo check if its only file name and add current dir
                if not os.path.dirname(halo_settings_path):
                    halo_settings_path = os.path.join(os.getcwd(),halo_settings_path)
        else:
            halo_settings_path =  os.path.join(os.getcwd(),'halo_settings.json')
        halo_settings = None
        try:
            halo_settings = Util.load_settings_file(halo_settings_path)
        except ConfigException as e:
            log("Error in HALO CLI settings file: " + str(e), "red")
            sys.exit(1)
        try:
            self.do_settings(halo_settings)
        except HaloCommandException as e:
            log("Error in HALO CLI Command : " + str(e), "red")
            sys.exit(1)
        except HaloPluginMngrException as e:
            log("Error in HALO CLI Plugin: " + str(e), "red")
            sys.exit(1)
        #if settings_error:
        #    log("Error in HALO CLI settings : " + str(settings_error), "red")
        return self.plugin_mngr.get_plugin_instances()

    def do_settings(self,settings):
        self.settings = settings # consider ImmutableDict(settings)
        self.proxy = HaloProxy(self.cli, self.variables, self.settings)
        self.do_plugins(settings)
        self.plugin_mngr = PluginMngr(self)

    def do_plugins(self,settings):
        self.plugins = [
            #"halocli.plugin.plugins.bian.extend.test_bian_plugin.Plugin",
            "halocli.plugin.plugins.bian.extend.extend_bian_plugin.Plugin",
            "halocli.plugin.plugins.bian.segregate.cqrs_bian_plugin.Plugin",
            "halocli.plugin.plugins.create.create_plugin.Plugin",
            "halocli.plugin.plugins.schema.schema_plugin.Plugin",
            "halocli.plugin.plugins.print.print_plugin.Plugin",
            "halocli.plugin.plugins.info.info_plugin.Plugin",
            "halocli.plugin.plugins.valid.valid_plugin.Plugin",
            "halocli.plugin.plugins.config.config_plugin.Plugin",
            "halocli.plugin.plugins.install.install_plugin.Plugin"
        ]
        if settings and "plugins" in settings:
            for p in settings["plugins"]:
                class_name = self.get_plugin_class(p)
                if class_name:
                    self.plugins.append(class_name)
                    self.names[class_name] = p

    def get_plugin_class(self, package_name):
        class_list =  Util.check_package_in_env(package_name)
        if len(class_list) > 1:
            raise HaloPluginClassException("too many plugin entry point classes package: " + package_name)
        if len(class_list) == 1:
            return class_list[0]
        raise HaloPluginClassException("plugin entry point class not found for package: "+package_name)

    def create_command_groups(self):
        return self.cmd.create_command_groups(self.plugins,cli)



if __name__ == "__main__":
    start()