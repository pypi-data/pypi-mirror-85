from __future__ import print_function
import sys
import os
import datetime
import logging
import json
from os.path import dirname
import importlib
import pkgutil
from halocli.exception import HaloPluginMngrException,HaloCommandException

logger = logging.getLogger(__name__)

discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules()
    if name.startswith('halo_')
}
#print("plugins:"+str(discovered_plugins))

class PluginMngr():
    plugins = {}
    plugin_commands = {}
    commands = {}
    counter = {}

    def __init__(self, halo):
        self.halo = halo
        self.plugins = {}
        self.plugin_commands = {}
        self.commands = {}
        self.counter = {}
        self.load_command_event_mappings()

    def add(self,event,diff):
        millis = diff.seconds * 1000
        millis += diff.microseconds / 1000
        self.counter[event] = millis

    def get_plugin_instances(self):
        arr = []
        for name in self.plugins.keys():
            arr.append(self.plugins[name])
        return arr

    def load_command_event_mappings(self):
        names = []
        if self.halo.plugins:
            for plugin in self.halo.plugins:
                p = self.init_plugin(plugin,self.halo)
                name = plugin
                if plugin in self.halo.names:
                    name = self.halo.names[plugin]
                if p:
                    if p.name:
                        if p.name not in names:
                            names.append(p.name)
                        else:
                            raise HaloPluginMngrException("name "+p.name+" for plugin:" + plugin+" already exists")
                    else:
                        raise HaloPluginMngrException("missing name for plugin:"+name)
                    self.plugins[plugin] = p
                    if p.commands:
                        p_commands = []
                        for c in p.commands:
                            if c not in self.commands:
                                self.commands[c] = p
                                p_commands.append({'name':c,'body':p.commands[c]})
                            else:
                                raise HaloCommandException('plugin: '+str(name) +' command "'+c+ '" already in use')
                        self.plugin_commands[p] = p_commands

    def get_plugins_for_command_event(self,command_event):
        if command_event:
            if command_event.command and command_event.command in self.commands:
                return self.commands[command_event.command]
        return None

    def get_command_events(self,plugin,command):
        arr = []
        if command in plugin.commands:
            return plugin.commands[command]['lifecycleEvents']
        return arr

    def run_command(self, ctx, command,args):
        if command and command in self.commands:
            plugin = self.commands[command]
            if plugin:
                plugin.run_plugin(args)
                for event in self.get_command_events(plugin,command):
                    start_date = datetime.datetime.now()
                    self.run(ctx,plugin,command,event,args)
                    diff = datetime.datetime.now() - start_date
                    #self.add(event,diff)
                logger.debug('finished plugin '+str(plugin))
                if ctx.obj.debug or ctx.obj.verbose:
                    self.halo.logy(args)
                    self.halo.logx(self.counter)
            return True
        return False

    def run(self,ctx,plugin,command,event,args):
        if ctx.obj.verbose:
            self.halo.cli.log("running command "+command+ " and event "+event)
        if plugin.hooks:
            #before:command:event
            for prefix in ['before:','','after:']:
                item = prefix+command+':'+event
                if item in plugin.hooks:
                    method = plugin.hooks[item]
                    start_date = datetime.datetime.now()
                    try:
                        method()
                    except AttributeError as e:
                        print(str(method)+" not found "+str(e))
                    diff = datetime.datetime.now() - start_date
                    self.add(item, diff)
                # do other plugins for event
                for p_name in self.plugins:
                    plug = self.plugins[p_name]
                    if plug != plugin and item in plug.hooks:
                        method = plug.hooks[item]
                        start_date = datetime.datetime.now()
                        try:
                            method()
                        except AttributeError as e:
                            print(str(method) + " not found " + str(e))
                        diff = datetime.datetime.now() - start_date
                        self.add(p_name+":"+item, diff)

    def init_plugin(self,plugin,halo):
        name = plugin
        if plugin in self.halo.names:
            name = self.halo.names[plugin]
        k = plugin.rfind(".")
        if k <= 0:
            raise Exception(plugin+": import class path error:" + name)
        module_name = plugin[:k]
        class_name = plugin[k + 1:]
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            raise HaloPluginMngrException(name+": import module error:" + str(e))
        else:
            try:
                class_ = getattr(module, class_name)
            except Exception as e:
                raise HaloPluginMngrException(name+": import class error:" + str(e))
            try:
                return class_(halo.proxy)
            except Exception as e:
                raise HaloPluginMngrException(name+": import class init error:" + str(e))



if __name__ == '__main__':
    #PluginMngr({},{}).run("halo.plugin.plugin.Plugin")
    class cli:
        def log(self,msg):
            print(msg)
    class halo:
        cli = cli()
        variables = None
        settings = object()
        plugins = ["halo.plugin.valid_plugin.Plugin","halo.plugin.plugin.Plugin"]
        def valid(self):
            self.cli.log("valid tests!")

    PluginMngr(halo(), {}).run_command({},'deployx')
    #PluginMngr(halo(), {}).run_command('valid')
