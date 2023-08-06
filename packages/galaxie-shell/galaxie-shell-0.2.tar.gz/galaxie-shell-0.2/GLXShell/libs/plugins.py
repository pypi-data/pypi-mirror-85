#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC APPLICATION_LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Shell Team, all rights reserved

import argparse
import cmd2

from GLXShell.libs.properties.plugins import GLXShPropertyPlugins
from GLXShell import APPLICATION_PLUGINS


def choices():
    to_return = []
    for plugin in APPLICATION_PLUGINS:
        if plugin and "name" in plugin:
            to_return.append(plugin["name"])
    return to_return


enable_parser = cmd2.Cmd2ArgumentParser()
enable_parser.add_argument("name", choices=choices())
disable_parser = cmd2.Cmd2ArgumentParser()
disable_parser.add_argument("name", choices=choices())
load_parser = cmd2.Cmd2ArgumentParser()
load_parser.add_argument("name", choices=choices())
unload_parser = cmd2.Cmd2ArgumentParser()
unload_parser.add_argument("name", choices=choices())
reload_parser = cmd2.Cmd2ArgumentParser()
reload_parser.add_argument("name", choices=choices())
plugins_parser = cmd2.Cmd2ArgumentParser(description="Plugins management")
plugins_subparsers = plugins_parser.add_subparsers(
    title="commands", help="a command it can be choose"
)


class GLXShPluginsManager(GLXShPropertyPlugins):
    def __init__(self, *args, **kwargs):
        GLXShPropertyPlugins.__init__(self)
        self.loaded_plugins = []

    def plugins_manager_control_config(self):
        if hasattr(self, "config") and self.config:
            have_change = False
            if "plugins" not in self.config.data:
                self.config.data["plugins"] = {}
                have_change = True
            for plugin in self.plugins:
                if plugin["name"] not in self.config.data["plugins"]:
                    self.config.data["plugins"][plugin["name"]] = {}
                    have_change = True
                if "enabled" not in self.config.data["plugins"][plugin["name"]]:
                    self.config.data["plugins"][plugin["name"]]["enabled"] = True
                    have_change = True
            if have_change:
                self.config.write_config()

    def load_plugins(self):
        self.plugins_manager_control_config()
        if (
            hasattr(self, "config")
            and self.config
            and hasattr(self, "shell")
            and self.shell
        ):
            for plugin in self.plugins:
                if self.config.data["plugins"][plugin["name"]]["enabled"]:
                    self.load(argparse.Namespace(name=plugin["name"]))

    @cmd2.as_subcommand_to("plugins", "enable", enable_parser)
    @cmd2.with_category("Plugins commands")
    def enable(self, ns: argparse.Namespace):
        """Enable at startup a plugin by it name and load it"""
        if (
            hasattr(self, "config")
            and self.config
            and hasattr(self, "shell")
            and self.shell
        ):
            for plugin in self.plugins:
                if ns.name == plugin["name"]:
                    if self.shell.debug:
                        self.shell.pwarning("ENABLE PLUGIN: {0}".format(plugin["name"]))
                    self.load(argparse.Namespace(name=ns.name))
                    if not self.config.data["plugins"][plugin["name"]]["enabled"]:
                        self.config.data["plugins"][plugin["name"]]["enabled"] = True
                        self.config.write_config()

    @cmd2.as_subcommand_to("plugins", "disable", disable_parser)
    @cmd2.with_category("Plugins commands")
    def disable(self, ns: argparse.Namespace):
        """Disable at startup a plugin by it name and unload it"""
        if (
            hasattr(self, "config")
            and self.config
            and hasattr(self, "shell")
            and self.shell
        ):
            for plugin in self.plugins:
                if ns.name == plugin["name"]:
                    if self.shell.debug:
                        self.shell.pwarning(
                            "DISABLE PLUGIN: {0}".format(plugin["name"])
                        )
                    self.unload(argparse.Namespace(name=ns.name))
                    if self.config.data["plugins"][plugin["name"]]["enabled"]:
                        self.config.data["plugins"][plugin["name"]]["enabled"] = False
                        self.config.write_config()

    @cmd2.as_subcommand_to("plugins", "load", load_parser)
    @cmd2.with_category("Plugins commands")
    def load(self, ns: argparse.Namespace):
        """Load a plugin by it name"""
        if (
            hasattr(self, "plugins")
            and self.plugins
            and hasattr(self, "shell")
            and self.shell
        ):
            for plugin in self.plugins:
                if ns.name == plugin["name"]:
                    if self.shell.debug:
                        self.shell.pwarning("LOAD PLUGIN: {0}".format(plugin["name"]))
                    plugin["object"].shell = self.shell
                    plugin["object"].load()
                    self.loaded_plugins.append(
                        "{0} {1}".format(plugin["name"], plugin["version"])
                    )

    @cmd2.as_subcommand_to("plugins", "unload", unload_parser)
    @cmd2.with_category("Plugins commands")
    def unload(self, ns: argparse.Namespace):
        """Unload a plugin by it name"""
        if (
            hasattr(self, "plugins")
            and self.plugins
            and hasattr(self, "shell")
            and self.shell
        ):
            for plugin in self.plugins:
                if ns.name == plugin["name"]:
                    if self.shell.debug:
                        self.shell.pwarning("UNLOAD PLUGIN: {0}".format(plugin["name"]))
                    plugin["object"].shell = self.shell
                    plugin["object"].unload()
                    try:
                        self.loaded_plugins.remove(
                            "{0} {1}".format(plugin["name"], plugin["version"])
                        )
                    except ValueError:
                        pass

    @cmd2.as_subcommand_to("plugins", "reload", reload_parser)
    @cmd2.with_category("Plugins commands")
    def reload(self, ns: argparse.Namespace):
        """Reload a plugin by it name"""
        if (
            hasattr(self, "plugins")
            and self.plugins
            and hasattr(self, "shell")
            and self.shell
        ):
            for plugin in self.plugins:
                if ns.name == plugin["name"]:
                    if self.shell.debug:
                        self.shell.pwarning("RELOAD PLUGIN: {0}".format(plugin["name"]))
                    plugin["object"].shell = self.shell
                    plugin["object"].reload()

    @cmd2.with_argparser(plugins_parser)
    @cmd2.with_category("Plugins")
    def do_plugins(self, ns: argparse.Namespace):
        handler = ns.cmd2_handler.get()  # pragma: no cover
        if handler is not None:  # pragma: no cover
            # Call whatever subcommand function was selected
            handler(ns)
        else:  # pragma: no cover
            # No subcommand was provided, so call help
            if hasattr(self, "shell") and self.shell:
                self.shell.perror("This command does nothing without sub-commands")
                self.shell.do_help("plugins")
