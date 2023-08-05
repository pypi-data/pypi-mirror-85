#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC APPLICATION_LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import os
import getpass
import socket

from GLXShell.libs.config import GLXShConfig


class GLXShPrompt(object):
    def __init__(self, *args, **kwargs):
        self.config = kwargs.get("config", GLXShConfig())

        have_change = False

        if "prompt" not in self.config.data:
            self.config.data["prompt"] = {}
            have_change = True

        if "show" not in self.config.data["prompt"]:
            self.config.data["prompt"]["show"] = {}
            have_change = True

        if have_change:
            self.config.write_config()

        self.__prompt_show_info = None
        self.__prompt_show_cursor = None

        try:
            self.prompt_show_cursor = self.config.data["prompt"]["show"]["cursor"]
        except KeyError:
            self.prompt_show_cursor = None
        try:
            self.prompt_show_info = self.config.data["prompt"]["show"]["info"]
        except KeyError:
            self.prompt_show_info = None

    @property
    def prompt_show_info(self):
        """
        That property is use in front on the user space configuration file, and be like a storage value wrapper.

        If the value change , the configuration file will be rewrite with fresh information's.

        :return: If ``True`` the prompt contain information's line.
        :rtype: bool
        """
        return self.__prompt_show_info

    @prompt_show_info.setter
    def prompt_show_info(self, value=None):
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError(
                "'prompt_show_info' property value must be a bool type or None"
            )
        if self.prompt_show_info != value:
            self.__prompt_show_info = value
        if (
            "info" not in self.config.data["prompt"]["show"]
            or self.config.data["prompt"]["show"]["info"] != value
        ):
            self.config.data["prompt"]["show"]["info"] = value
            self.config.write_config()

    @property
    def prompt_show_cursor(self):
        """
        That property is use in front on the user space configuration file, and be like a storage value wrapper.

        If the value change , the configuration file will be rewrite with fresh information's.

        :return: If ``True`` the prompt display something before the cursor.
        :rtype: bool
        """
        return self.__prompt_show_cursor

    @prompt_show_cursor.setter
    def prompt_show_cursor(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError(
                "'prompt_show_cursor' property value must be a bool type or None"
            )
        if self.prompt_show_cursor != value:
            self.__prompt_show_cursor = value
        if (
            "cursor" not in self.config.data["prompt"]["show"]
            or self.config.data["prompt"]["show"]["cursor"] != value
        ):
            self.config.data["prompt"]["show"]["cursor"] = value
            self.config.write_config()

    def onchange_prompt_show_cursor(self, param_name, old_value, new_value):
        """Internal function call by ``cmd2`` python module during a ``set``"""
        pass

    def onchange_prompt_show_info(self, param_name, old_value, new_value):
        """Internal function call by ``cmd2`` python module during a ``set``"""
        pass

    @property
    def prompt_env_is_virtual(self):
        """
        Return ``True`` if a virtual environment is detected.

        :return: ``True`` if environments variables *VIRTUAL_ENV* or *CONDA_DEFAULT_ENV* are set
        :rtype: bool
        """
        if os.environ.get("VIRTUAL_ENV") or os.environ.get("CONDA_DEFAULT_ENV"):
            return True
        else:
            return False

    @property
    def prompt_env_name_text(self):
        """
        It property return the activated virtual environment surrounded by parentheses

        *VIRTUAL_ENV* and *CONDA_DEFAULT_ENV* environments variables are used during venv detection.

        **Example**

        .. code:: text

            (venv)

        :return: the basename of directory announced by var *VIRTUAL_ENV* or *CONDA_DEFAULT_ENV*
        :rtype: str
        """
        if os.environ.get("VIRTUAL_ENV") or os.environ.get("CONDA_DEFAULT_ENV"):
            env_path = os.environ.get("VIRTUAL_ENV", "")
            if len(env_path) == 0:
                env_path = os.environ.get("CONDA_DEFAULT_ENV", "")

            return "({env_name}) ".format(env_name=os.path.basename(env_path))
        else:
            return ""

    @property
    def prompt_username_text(self):
        """
        That property return the ``getpass.getuser()`` value. That is used by the prompt for display username.

        **Example**

        .. code:: text

            me

        :return: ``getpass.getuser()``
        :rtype: str
        """
        return getpass.getuser()

    @property
    def prompt_hostname_text(self):
        """
        That property return the ``socket.gethostname()`` value. That is used by the prompt for display hostname.

        **Example**

        .. code:: text

            localdomain

        :return: ``socket.gethostname()``
        :rtype: str
        """
        return socket.gethostname()

    @property
    def prompt_path_text(self):
        """
        That property return the current working directory. That is used by the prompt for display path.

        .. note:: the path is user expanded.

        **Example**

        .. code:: text

            ~/galaxie-shell/docs

        :return: current working directory
        :rtype: str
        """
        return os.getcwd().replace(os.path.realpath(os.path.expanduser("~")), "~")

    @property
    def prompt_symbol_text(self):
        """
        If UID = 0 return #

        If not return $

        :return: # if ``os.getuid() == 0`` else $
        :rtype: str
        """
        if os.getuid() == 0:  # pragma: no cover
            return "#"
        else:
            return "$"

    @property
    def prompt_cursor_text(self):
        """
        That property return the character just before cursor.

        **Example**

        .. code:: text

            >

        :return: char just before the blinking cursor
        :rtype: str
        """
        return ">"

    @property
    def prompt_to_display(self):
        """
        The function is use by the GLXShell class for get prompt text to display.

        That is responsibility of GLXShellPrompt class to know what display where GLXShell class only get the text.

        **Example**

        .. code:: text

            (venv) me@localdomain:~/galaxie-shell/docs $
            >

        :return: a big string it correspond to the entire prompt to display
        :rtype: str
        """
        prompt = []
        if self.prompt_show_info:
            prompt.append(
                "{venv}{username}@{hostname}:{path} {symbol} ".format(
                    venv=self.prompt_env_name_text,
                    username=self.prompt_username_text,
                    hostname=self.prompt_hostname_text,
                    path=self.prompt_path_text,
                    symbol=self.prompt_symbol_text,
                )
            )
        if self.prompt_show_cursor:
            prompt.append("{cursor} ".format(cursor=self.prompt_cursor_text))

        return "\n".join(prompt)
