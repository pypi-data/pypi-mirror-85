#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC APPLICATION_LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Shell Team, all rights reserved

import os
import json

from GLXShell.libs.xdg_base_directory import XDGBaseDirectory


class Singleton(type):
    def __init__(cls, name, bases, dictionary):
        super(Singleton, cls).__init__(name, bases, dictionary)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args)
        return cls.instance


class GLXShConfig(XDGBaseDirectory, metaclass=Singleton):
    """
    Config provide method to work with Galaxie Shell configuration file.

    The configuration file respect XDG standard, then the configuration file is store on standardized path.
    (it can be change but by default that is ``~/.config/glxsh/config.json``)

    GLXShConfig have two settings views, one store on a configuration file , and one store on ``data`` property.

    ``data`` property is the property use by each class for get the setting, that is responsibility to each
    class's to verify if those setting have change then call ``GLXShConfig.write_config()`` in case.

    .. note:: Config is a Straightforward implementation of the Singleton Pattern.

    Configuration file example: ~/.config/glxsh/config.json

    .. code:: json

        {
            "intro": {
                "show": {
                    "exec": true,
                    "holotape": false,
                    "license": false,
                    "loader": false,
                    "memory_free": true,
                    "memory_total": true,
                    "rom": true,
                    "spacing": false,
                    "title": true
                }
            },
            "plugins": {
                "builtins": {
                    "enabled": true
                }
            },
            "prompt": {
                "show": {
                    "cursor": true,
                    "info": true
                }
            }
        }
    """

    def __init__(self):
        XDGBaseDirectory.__init__(self)

        self.__file = None
        self.__data = None

        self.file = None
        self.data = None

        self.touch_config()
        self.load_config()

    @property
    def file(self):
        """
        Property it store configuration file path

        Note: Default is XDGBaseDirectory/glxsh

        :return: the config file path
        :rtype: str
        """
        return self.__file

    @file.setter
    def file(self, value=None):
        """
        Set the ``file`` property value

        Note: if ``file`` property value is set to ``None``
        it restore default value provide by XDGBaseDirectory join by APPLICATION_NAME value fount in __init__.py on the
        root of the project.

        :param value: the config file path
        :type value: str or None
        """
        if value is None:
            value = os.path.join(self.config_path, "config.json")
        if type(value) != str:
            raise TypeError("'config_file' property value must be a str type or None")
        if value != self.file:
            self.__file = value

    @property
    def data(self):
        """
        A dictionary it contain all the setting. That property is for get or store data setting.

        .. note:: If ``data`` property value is ``None``, it restore a empty dictionary setting, but not write it.

        :return: the setting
        :rtype: dict
        """
        return self.__data

    @data.setter
    def data(self, value=None):
        """
        Set the ``data`` property

        :param value: the setting
        :return: dict or None
        :raise TypeError: When ``data`` property value is not dict type or None
        """
        if value is None:
            value = {}
        if type(value) != dict:
            raise TypeError("'data' property value must be a dict type or None")
        if self.data != value:
            self.__data = value

    def touch_config(self):
        """
        Create directories where store the configuration file and if the config file do not exist
        create one with a empty dictionary.

        The configuration file path is get by ``file`` property
        """
        if not os.path.exists(os.path.dirname(self.file)):
            os.makedirs(os.path.dirname(self.file))
        if not os.path.exists(self.file):
            with open(self.file, "w") as outfile:
                json.dump({}, outfile)

    def load_config(self):
        """
        Load the configuration file and update ``data`` property, the configuration file path is get by
        ``file`` property
        """
        with open(self.file, "r") as json_data_file:
            self.data.update(json.load(json_data_file))

    def write_config(self):
        """
        Write ``data`` property value content inside the configuration file path get by
        ``file`` property
        """
        with open(self.file, "w") as outfile:
            json.dump(self.data, outfile, sort_keys=True, indent=4)
