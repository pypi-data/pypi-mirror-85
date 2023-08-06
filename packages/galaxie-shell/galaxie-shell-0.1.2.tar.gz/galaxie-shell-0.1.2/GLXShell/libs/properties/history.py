#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC APPLICATION_LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import os

from GLXShell.libs.xdg_base_directory import XDGBaseDirectory


class GLXShPropertyHistory(XDGBaseDirectory):
    def __init__(self):
        XDGBaseDirectory.__init__(self)
        self.__persistent_history_file = None
        self.__persistent_history_length = None

        self.persistent_history_file = None
        self.persistent_history_length = None

    @property
    def persistent_history_file(self):
        return self.__persistent_history_file

    @persistent_history_file.setter
    def persistent_history_file(self, value=None):
        if value is None or value == "":
            value = os.path.join(self.config_path, "history")
        if value != self.persistent_history_file:
            self.__persistent_history_file = value

    @property
    def persistent_history_length(self):
        return self.__persistent_history_length

    @persistent_history_length.setter
    def persistent_history_length(self, value=None):
        if value is None:
            value = 500
        if type(value) != int:
            raise TypeError(
                "'persistent_history_length' property value must be int type or None"
            )
        if not value >= 0:
            raise ValueError(
                "'persistent_history_length' property value must be positive int"
            )
        if self.persistent_history_length != value:
            self.__persistent_history_length = value
