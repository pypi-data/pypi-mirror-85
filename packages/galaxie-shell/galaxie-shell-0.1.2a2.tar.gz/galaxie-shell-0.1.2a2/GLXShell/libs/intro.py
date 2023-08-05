# !/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC APPLICATION_LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Shell Team, all rights reserved

import os
import sys
import platform
from shutil import get_terminal_size

from GLXShell import APPLICATION_VERSION
from GLXShell import APPLICATION_NAME
from GLXShell import APPLICATION_LICENSE
from GLXShell.libs.config import GLXShConfig


def get_memory_total():
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    except ValueError:  # pragma: no cover
        return 0


def get_memory_available():
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_AVPHYS_PAGES")
    except ValueError:  # pragma: no cover
        return 0


def get_size(size, suffix="B"):
    """
    Scale bytes to its proper format

    **Example:**
        1253656 => '1.20MB'
        1253656678 => '1.17GB'

    :param size: bytes size to convert
    :type size: int
    :param suffix: what suffix is add at the end of the returned value
    :type: str
    """
    for unit in ["", "K", "M", "G", "T", "P"]:
        if size < 1024:
            return f"{size:.2f}{unit}{suffix}"
        size /= 1024


class GLXShIntro(object):
    """
    It Class have responsibility to provide text to display with system information's.

    The class contain many property for user configuration, for let him capability to control it class setting from the
    ``glxsh`` , configuration file or from anywhere on the code.

    The entry point is the function ``intro_to_display()``

    **config**: ``GLXShConfig``
        A instance of GLXShConfig or None for create a new one.
        Generally you haven't to set it, that is use by tests for not destroy user space config during tests.
    **rows**: ``int``
        The terminal rows number, actually not use
    **columns**: ``int``
        The terminal columns

    """

    def __init__(self, *args, **kwargs):
        self.__intro_show_title = None
        self.__intro_show_spacing = None
        self.__intro_show_license = None
        self.__intro_show_loader = None
        self.__intro_show_exec = None
        self.__intro_show_memory_total = None
        self.__intro_show_memory_free = None
        self.__intro_show_holotape = None
        self.__intro_show_rom = None

        self.config = kwargs.get("config", GLXShConfig())

        have_change = False
        if "intro" not in self.config.data:
            self.config.data["intro"] = {}
            have_change = True

        if "show" not in self.config.data["intro"]:
            self.config.data["intro"]["show"] = {}
            have_change = True

        if have_change:
            self.config.write_config()

        try:
            self.intro_show_exec = self.config.data["intro"]["show"]["exec"]
        except KeyError:
            self.intro_show_exec = None
        try:
            self.intro_show_holotape = self.config.data["intro"]["show"]["holotape"]
        except KeyError:
            self.intro_show_holotape = None
        try:
            self.intro_show_license = self.config.data["intro"]["show"]["license"]
        except KeyError:
            self.intro_show_license = None
        try:
            self.intro_show_loader = self.config.data["intro"]["show"]["loader"]
        except KeyError:
            self.intro_show_loader = None
        try:
            self.intro_show_memory_free = self.config.data["intro"]["show"][
                "memory_free"
            ]
        except KeyError:
            self.intro_show_memory_free = None
        try:
            self.intro_show_memory_total = self.config.data["intro"]["show"][
                "memory_total"
            ]
        except KeyError:
            self.intro_show_memory_total = None
        try:
            self.intro_show_rom = self.config.data["intro"]["show"]["rom"]
        except KeyError:
            self.intro_show_rom = None
        try:
            self.intro_show_spacing = self.config.data["intro"]["show"]["spacing"]
        except KeyError:
            self.intro_show_spacing = None
        try:
            self.intro_show_title = self.config.data["intro"]["show"]["title"]
        except KeyError:
            self.intro_show_title = None

    @property
    def intro_line_exec(self):
        """
        That property return a formatted line it contain a upper string with python env and version information's.

        They information's are search on environment vars *VIRTUAL_ENV* or *CONDA_DEFAULT_ENV* and module ``sys``
        python module.

        Example:

        .. code:: text

            EXEC VENV PYTHON 3.7.3

        :return: line formatted with python env and version information's
        :rtype: str
        """
        if os.environ.get("VIRTUAL_ENV") or os.environ.get("CONDA_DEFAULT_ENV"):
            env_path = os.environ.get("VIRTUAL_ENV", "")
            if len(env_path) == 0:
                env_path = os.environ.get("CONDA_DEFAULT_ENV", "")
            exec_venv = "({env_name}) ".format(
                env_name=os.path.basename(env_path)
            ).upper()
        else:
            exec_venv = ""
        return "EXEC {exec_venv}PYTHON {python_version_major}.{python_version_minor}.{python_version_micro}".format(
            exec_venv=exec_venv,
            python_version_major=sys.version_info.major,
            python_version_minor=sys.version_info.minor,
            python_version_micro=sys.version_info.micro,
        )

    @property
    def intro_line_holotape(self):
        """
        That property return a formatted line it contain a upper string with style text.

        It will normally be use for plugins information's

        Example:

        .. code:: text

            NO HOLOTAPE FOUND

        :return: line formatted with style
        :rtype: str
        """
        return "NO HOLOTAPE FOUND"

    @property
    def intro_line_license(self):
        """
        That property return a formatted line it contain a upper string with style text.

        It will normally be use for plugins information's

        Example:

        .. code:: text

            GNU GENERAL PUBLIC APPLICATION_LICENSE GPL-3.0

        :return: line formatted with style
        :rtype: str
        """
        return APPLICATION_LICENSE.upper()

    @property
    def intro_line_loader(self):
        """
        That property return a formatted line it contain a system information text.

        Information's are found on ``platform`` python module.

        Example:

        .. code:: text

            LOADER #1 SMP DEBIAN 4.19.146-1 (2020-09-17)

        :return: line formatted with style
        :rtype: str
        """
        return "LOADER {0}".format(platform.version().upper())

    @property
    def intro_line_memory_free(self):
        """
        That property return a formatted line it contain a system memory free information's text.

        Example:

        .. code:: text

            21.60GB FREE

        :return: memory free information's
        :rtype: str
        """
        return "{mem_available} FREE".format(
            mem_available=get_size(get_memory_available())
        )

    @property
    def intro_line_memory_total(self):
        """
        That property return a formatted line it contain a system memory total information's text.

        Example:

        .. code:: text

            31.36GB RAM SYSTEM

        :return: memory total information's
        :rtype: str
        """
        return "{mem_total} RAM SYSTEM".format(mem_total=get_size(get_memory_total()))

    @property
    def intro_line_rom(self):
        """
        That property return a formatted line it contain a upper string with style text.

        It return plugins information's

        Example:

        .. code:: text

            LOAD APPLICATION_PLUGINS(1): DEITRIX 303

        :return: plugins information's
        :rtype: str
        """
        value = 0
        value_2 = ""
        if hasattr(self, "shell") and self.shell:
            if hasattr(self.shell, "loaded_plugins"):
                value = len(self.shell.loaded_plugins)
                value_2 = ", ".join(self.shell.loaded_plugins)

        return "LOAD APPLICATION_PLUGINS({0}): {1}".format(value, value_2.upper())

    @property
    def intro_line_title(self):
        """
        That property return a string formatted as a line it contain a upper string with application and version
        information's.

        They information's are search in ``__init__.py`` file on the root of the project.

        .. code:: python

            APPLICATION_NAME= "SuperShell"
            APPLICATION_VERSION= "42.1"

        The ``columns`` property value is use to calculate the width and title position.

        Example:

        .. code:: text

            ************************** SUPERSHELL V42.1 ****************************

        :return: line formatted with ``title`` property information's
        :rtype: str
        """
        title = "{app_name} V{version}".format(
            app_name=APPLICATION_NAME.upper(), version=APPLICATION_VERSION.upper()
        )
        columns, rows = get_terminal_size()
        return "{text_inner} {text} {text_outer}".format(
            text=title,
            text_inner="*" * int((int(columns) / 2) - (len(title) / 2) - 1),
            text_outer="*" * int((int(columns) / 2) - (len(title) / 2) - 1),
        )

    @property
    def intro_show_exec(self):
        """
        That property is use in front on the user space configuration file, and be like a storage value wrapper.

        If the value change , the configuration file will be rewrite with fresh information's.

        :return: If ``True`` the EXEC line is allow to be display.
        :rtype: bool
        """
        return self.__intro_show_exec

    @intro_show_exec.setter
    def intro_show_exec(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'exec' property value must be a bool type or None")
        if self.intro_show_exec != value:
            self.__intro_show_exec = value
        if (
            "exec" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["exec"] != value
        ):
            self.config.data["intro"]["show"]["exec"] = value
            self.config.write_config()

    @property
    def intro_show_holotape(self):
        """
        That property is use in front on the user space configuration file, and be like a storage value wrapper.

        If the value change , the configuration file will be rewrite with fresh information's.

        :return: If ``True`` the EXEC line is allow to be display.
        :rtype: bool
        """
        return self.__intro_show_holotape

    @intro_show_holotape.setter
    def intro_show_holotape(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'holotape' property value must be a bool type or None")
        if self.intro_show_holotape != value:
            self.__intro_show_holotape = value
        if (
            "holotape" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["holotape"] != value
        ):
            self.config.data["intro"]["show"]["holotape"] = value
            self.config.write_config()

    @property
    def intro_show_license(self):
        """
        That property is use in front on the user space configuration file, and be like a storage value wrapper.

        If the value change , the configuration file will be rewrite with fresh information's.

        :return: If ``True`` the APPLICATION_LICENSE line is allow to be display.
        :rtype: bool
        """
        return self.__intro_show_license

    @intro_show_license.setter
    def intro_show_license(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError(
                "'show_license_line' property value must be a bool type or None"
            )
        if self.intro_show_license != value:
            self.__intro_show_license = value
        if (
            "license" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["license"] != value
        ):
            self.config.data["intro"]["show"]["license"] = value
            self.config.write_config()

    @property
    def intro_show_loader(self):
        """
        That property is use in front on the user space configuration file, and be like a storage value wrapper.

        If the value change , the configuration file will be rewrite with fresh information's.

        :return: If ``True`` the LOADER line is allow to be display.
        :rtype: bool
        """
        return self.__intro_show_loader

    @intro_show_loader.setter
    def intro_show_loader(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError(
                "'show_line_loader' property value must be a bool type or None"
            )
        if self.intro_show_loader != value:
            self.__intro_show_loader = value
        if (
            "loader" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["loader"] != value
        ):
            self.config.data["intro"]["show"]["loader"] = value
            self.config.write_config()

    @property
    def intro_show_memory_free(self):
        """
        That property is use in front on the user space configuration file, and be like a storage value wrapper.

        If the value change , the configuration file will be rewrite with fresh information's.

        :return: If ``True`` the MEMORY FREE line is allow to be display.
        :rtype: bool
        """
        return self.__intro_show_memory_free

    @intro_show_memory_free.setter
    def intro_show_memory_free(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError(
                "'show_line_memory_free' property value must be a bool type or None"
            )
        if self.intro_show_memory_free != value:
            self.__intro_show_memory_free = value
        if (
            "memory_free" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["memory_free"] != value
        ):
            self.config.data["intro"]["show"]["memory_free"] = value
            self.config.write_config()

    @property
    def intro_show_memory_total(self):
        """
        That property is use in front on the user space configuration file, and be like a storage value wrapper.

        If the value change , the configuration file will be rewrite with fresh information's.

        :return: If ``True`` the MEMORY TOTAL line is allowed to display.
        :rtype: bool
        """
        return self.__intro_show_memory_total

    @intro_show_memory_total.setter
    def intro_show_memory_total(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError(
                "'show_memory_total_line' property value must be a bool type or None"
            )
        if self.intro_show_memory_total != value:
            self.__intro_show_memory_total = value
        if (
            "memory_total" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["memory_total"] != value
        ):
            self.config.data["intro"]["show"]["memory_total"] = value
            self.config.write_config()

    @property
    def intro_show_rom(self):
        """
        That property is use in front on the user space configuration file, and be like a storage value wrapper.

        If the value change , the configuration file will be rewrite with fresh information's.

        :return: If ``True`` the ROM line is allowed to be display.
        :rtype: bool
        """
        return self.__intro_show_rom

    @intro_show_rom.setter
    def intro_show_rom(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError(
                "'show_line_rom' property value must be a bool type or None"
            )
        if self.intro_show_rom != value:
            self.__intro_show_rom = value
        if (
            "rom" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["rom"] != value
        ):
            self.config.data["intro"]["show"]["rom"] = value
            self.config.write_config()

    @property
    def intro_show_spacing(self):
        return self.__intro_show_spacing

    @intro_show_spacing.setter
    def intro_show_spacing(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError(
                "'intro_show_spacing' property value must be a bool type or None"
            )
        if self.intro_show_spacing != value:
            self.__intro_show_spacing = value
        if (
            "spacing" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["spacing"] != value
        ):
            self.config.data["intro"]["show"]["spacing"] = value
            self.config.write_config()

    @property
    def intro_show_title(self):
        """
        That property is use in front on the user space configuration file, and be like a storage value wrapper.

        If the value change , the configuration file will be rewrite with fresh information's.

        :return: If ``True`` the TITLE line is allowed to be display.
        :rtype: bool
        """
        return self.__intro_show_title

    @intro_show_title.setter
    def intro_show_title(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError(
                "'show_line_title' property value must be a bool type or None"
            )
        if self.intro_show_title != value:
            self.__intro_show_title = value
        if (
            "title" not in self.config.data["intro"]["show"]
            or self.config.data["intro"]["show"]["title"] != value
        ):
            self.config.data["intro"]["show"]["title"] = value
            self.config.write_config()

    def onchange_intro_show_exec(self, param_name, old_value, new_value):
        """Internal function call by ``cmd2`` python module during a ``set``"""
        pass

    def onchange_intro_show_holotape(self, param_name, old_value, new_value):
        """Internal function call by ``cmd2`` python module during a ``set``"""
        pass

    def onchange_intro_show_license(self, param_name, old_value, new_value):
        """Internal function call by ``cmd2`` python module during a ``set``"""
        pass

    def onchange_intro_show_loader(self, param_name, old_value, new_value):
        """Internal function call by ``cmd2`` python module during a ``set``"""
        pass

    def onchange_intro_show_memory_free(self, param_name, old_value, new_value):
        """Internal function call by ``cmd2`` python module during a ``set``"""
        pass

    def onchange_intro_show_memory_total(self, param_name, old_value, new_value):
        """Internal function call by ``cmd2`` python module during a ``set``"""
        pass

    def onchange_intro_show_rom(self, param_name, old_value, new_value):
        """Internal function call by ``cmd2`` python module during a ``set``"""
        pass

    def onchange_intro_show_spacing(self, param_name, old_value, new_value):
        """Internal function call by ``cmd2`` python module during a ``set``"""
        pass

    def onchange_intro_show_title(self, param_name, old_value, new_value):
        """Internal function call by ``cmd2`` python module during a ``set``"""
        pass

    @property
    def intro_to_display(self):
        """
        The function is use by the GLXShell class for get intro text to display.

        That is responsibility of GLXShellIntro class to know what display where GLXShell class only get the text.

        Example:

        .. code:: text

            ************************** SUPERSHELL V42.1 ****************************


            EXEC VENV PYTHON 3.7.3
            LOADER #1 SMP DEBIAN 4.19.146-1 (2020-09-17)
            31.36GB RAM SYSTEM
            20.85GB FREE
            LOAD ROM(1): DEITRIX 303

            (venv) me@localdomain:~/galaxie-shell $
            >

        :return: a big string it correspond to the entire intro to display
        :rtype: str
        """

        to_return = []

        if self.intro_show_title:
            to_return.append(self.intro_line_title)
            if self.intro_show_spacing:
                to_return.append("")
                to_return.append("")

        if self.intro_show_license:
            to_return.append(self.intro_line_license)

        if self.intro_show_loader:
            to_return.append(self.intro_line_loader)

        if self.intro_show_exec:
            to_return.append(self.intro_line_exec)

        if self.intro_show_memory_total:
            to_return.append(self.intro_line_memory_total)

        if self.intro_show_memory_free:
            to_return.append(self.intro_line_memory_free)

        if self.intro_show_holotape:
            to_return.append(self.intro_line_holotape)

        if self.intro_show_rom:
            to_return.append(self.intro_line_rom)

        if self.intro_show_spacing:
            to_return.append("")

        return "\n".join(to_return)
