#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC APPLICATION_LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Shell Team, all rights reserved

# Inspired by:
import os
import stat
import io
import random

from GLXShell import APPLICATION_NAME


def new_id():
    """
    Generate a ID like 'E59E8457', two chars by two chars it's a random HEX

    **Default size:**
        8
    **Default chars:**
        'ABCDEF0123456789'
    **Benchmark**
       +----------------+---------------+----------------------------------------------+
       | **Iteration**  | **Duration**  | **CPU Information**                          |
       +----------------+---------------+----------------------------------------------+
       | 10000000       | 99.114s       | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+
       | 1000000        | 9.920s        | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+
       | 100000         | 0.998s        | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+
       | 10000          | 0.108s        | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+

    :return: a string it represent a unique ID
    :rtype: str
    """
    return "%02x%02x%02x%02x".upper() % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def get_os_temporary_dir():
    """
    Get the OS default dir , the better as it can.

    It suppose to be cross platform

    :return: A tmp dir path
    :rtype: str
    """
    text_flags = os.O_RDWR | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        text_flags |= os.O_NOFOLLOW

    bin_flags = text_flags
    if hasattr(os, "O_BINARY"):  # pragma: no cover
        bin_flags |= os.O_BINARY

    directory_list = list()

    # First, try the environment.
    for envname in "TMPDIR", "TEMP", "TMP":
        dirname = os.getenv(envname)
        if dirname:
            directory_list.append(os.path.abspath(dirname))

    directory_list.extend(["/tmp", "/var/tmp", "/usr/tmp"])

    for directory in directory_list:
        if directory != os.path.curdir:
            directory = os.path.abspath(directory)

        filename = os.path.join(
            directory, "{0}-{1}{2}".format(APPLICATION_NAME, new_id(), ".cp")
        )
        try:
            fd = os.open(filename, bin_flags, 0o600)
            try:
                try:
                    with io.open(fd, "wb", closefd=False) as fp:
                        fp.write(b"Test")
                finally:
                    os.close(fd)
            finally:
                os.unlink(filename)
            return directory

        except PermissionError:  # pragma: no cover
            break  # no point trying more names in this directory
        except OSError:  # pragma: no cover
            break  # no point trying more names in this directory
    raise FileNotFoundError(  # pragma: no cover
        "No usable temporary directory found in %s" % directory_list
    )


def control_directory(directory=None, mode=0o700):
    """
    Internal function it create a directory if not exist

    :param directory:
    :type: str
    :param mode: the permission mode of the directory if created example:``0o700``
    :type mode: int
    :return: the directory path or None
    :rtype: str
    :raise TypeError: when ``directory`` is not a str type
    :raise TypeError: when ``directory`` is not a int type
    """
    if type(directory) != str:
        raise TypeError("directory must be a str type")

    if type(mode) != int:
        raise TypeError("mode must be a int type")

    if not os.path.isdir(directory):
        os.makedirs(directory, mode=mode)

    return directory


class XDGBaseDirectory(object):
    def __init__(self):
        self.__resource = None

        self.set_resource(APPLICATION_NAME)

    @property
    def xdg_data_home(self):
        """
        $XDG_DATA_HOME defines the base directory relative to which user specific data files should be stored.

        If $XDG_DATA_HOME is either not set or empty, a default equal to $HOME/.local/share should be used.

        :return: base directory relative to which user specific data files
        :rtype: str
        """
        if os.environ.get("XDG_DATA_HOME") and os.path.isabs(
            os.environ.get("XDG_DATA_HOME")
        ):
            return os.environ.get("XDG_DATA_HOME")

        return control_directory(
            os.path.join(os.path.expanduser("~"), ".local", "share")
        )

    @property
    def xdg_config_home(self):
        """
        $XDG_CONFIG_HOME defines the base directory relative to which user specific configuration files
        should be stored.

        If $XDG_CONFIG_HOME is either not set or empty, a default equal to $HOME/.config should be used.

        :return: base directory relative to which user specific configuration files
        :rtype: str
        """
        if os.environ.get("XDG_CONFIG_HOME") and os.path.isabs(
            os.environ.get("XDG_CONFIG_HOME")
        ):
            return os.environ.get("XDG_CONFIG_HOME")

        return control_directory(os.path.join(os.path.expanduser("~"), ".config"))

    @property
    def xdg_data_dirs(self):
        """
        $XDG_DATA_DIRS defines the preference-ordered set of base directories to search for data files in addition to
        the $XDG_DATA_HOME base directory.

        The directories in $XDG_DATA_DIRS should be separated with a colon ':'.

        If $XDG_DATA_DIRS is either not set or empty, a value equal to /usr/local/share/:/usr/share/ should be used.

        :return: preference-ordered set of base directories to search for data files separated with a colon ':'
        :rtype: str
        """
        if os.environ.get("XDG_DATA_DIRS"):
            tmp_list = [self.xdg_data_home]
            for path in os.environ.get("XDG_DATA_DIRS").split(":"):
                if os.path.isabs(path):
                    tmp_list.append(control_directory(path))

            return ":".join(tmp_list)

        return "/usr/local/share/:/usr/share/"

    @property
    def xdg_config_dirs(self):
        """
        $XDG_CONFIG_DIRS defines the preference-ordered set of base directories to search for configuration files
        in addition to the $XDG_CONFIG_HOME base directory.

        The directories in $XDG_CONFIG_DIRS should be separated with a colon ':'.

        If $XDG_CONFIG_DIRS is either not set or empty, a value equal to /etc/xdg should be used.

        :return: preference-ordered set of base directories to search for configuration files separated with a colon ':'
        :rtype: str
        """
        if os.environ.get("XDG_CONFIG_DIRS"):
            tmp_list = [self.xdg_config_home]
            for path in os.environ.get("XDG_CONFIG_DIRS").split(":"):
                if os.path.isabs(path) and path not in tmp_list:
                    tmp_list.append(control_directory(path))

            return ":".join(tmp_list)

        return ":".join([self.xdg_config_home, "/etc/xdg"])

    @property
    def xdg_cache_home(self):
        """
        $XDG_CACHE_HOME defines the base directory relative to which user specific non-essential data files
        should be stored.

        If $XDG_CACHE_HOME is either not set or empty, a default equal to $HOME/.cache should be used.

        :return: base directory relative to which user specific non-essential data files
        :rtype: str
        """
        if os.environ.get("XDG_CACHE_HOME") and os.path.isabs(
            os.environ.get("XDG_CACHE_HOME")
        ):
            return os.environ.get("XDG_CACHE_HOME")
        return os.path.join(os.path.expanduser("~"), ".cache")

    @property
    def xdg_runtime_dir(self):
        """
        $XDG_RUNTIME_DIR defines the base directory relative to which user-specific non-essential runtime files and
        other file objects (such as sockets, named pipes, ...) should be stored.

        If $XDG_RUNTIME_DIR is not set applications should fall back to a replacement directory with similar
        capabilities and print a warning message.

        Applications should use this directory for communication and synchronization purposes and should not
        place larger files in it, since it might reside in runtime memory and cannot necessarily be swapped out to disk.

        :return: base directory relative to which user-specific non-essential runtime files
        :rtype: str
        """
        if os.environ.get("XDG_RUNTIME_DIR") and os.path.isabs(
            os.environ.get("XDG_RUNTIME_DIR")
        ):
            return os.environ["XDG_RUNTIME_DIR"]

        fallback = os.path.join(
            get_os_temporary_dir(),
            "glxcurses-runtime-dir-fallback-{0}".format(os.geteuid()),
        )

        if os.path.isfile(fallback):
            os.remove(fallback)

        if os.path.islink(fallback):
            os.unlink(fallback)

        if os.path.isdir(fallback):
            if os.stat(fallback).st_uid != os.geteuid() or (
                os.stat(fallback).st_mode & (stat.S_IRWXG | stat.S_IRWXO)
            ):
                os.rmdir(fallback)

        return control_directory(fallback)

    @property
    def resource(self):
        """
        ``resource`` should normally be the name of your application or a shared resource.

        :return: name of your application or a shared resource
        :rtype: str
        """
        return self.__resource

    @resource.setter
    def resource(self, value):
        """
        Set the ``resource`` property value.

        You should not use it setter directly, then you should take a look to ``set_resource`` function

        :param value: name of your application or a shared resource
        :type value: str
        :raise TypeError: When ``resource`` value is not a str type
        """
        if type(value) != str:
            raise TypeError("'resource' value must be a str")
        if self.resource != value:
            self.__resource = value

    def set_resource(self, *resource):
        """
        Set the ``resource`` property value.

        :param resource: should normally be the name of your application
        :type resource: tuple like 'Hello', '42'
        :raise AssertionError: If when join the tuple start by os.path.sep typically ``/``
        """
        resource = os.path.join(*resource)
        if resource.startswith(os.path.sep):
            raise AssertionError(
                "'resource' value can not start by {0}".format(os.path.sep)
            )
        self.resource = resource

    @property
    def config_path(self):
        """
        Ensure ``$XDG_CONFIG_HOME/<resource>/`` exists, and return its path.

        :return: ``$XDG_CONFIG_HOME/<resource>/`` path
        :rtype: str
        """
        return control_directory(os.path.join(self.xdg_config_home, self.resource))

    @property
    def config_paths(self):
        """
        Returns an iterator which gives each directory named 'resource' in the configuration search path.

        Information provided by earlier directories should take precedence over later ones, and the user-specific
        config dir comes first.

        :return: pre-ordered set of base directories to search for configuration files directory for ``resource``
        :rtype: list
        """
        tmp_list = [self.config_path]
        for config_dir in self.xdg_config_dirs.split(":"):
            if os.path.exists(os.path.join(config_dir, self.resource)):
                if os.path.join(config_dir, self.resource) not in tmp_list:
                    tmp_list.append(os.path.join(config_dir, self.resource))
        return tmp_list

    @property
    def data_path(self):
        """
        Ensure ``$XDG_DATA_HOME/<resource>/`` exists, and return its path.

        :return: ``$XDG_DATA_HOME/<resource>/`` path
        :rtype: str
        """
        return control_directory(os.path.join(self.xdg_data_home, self.resource))

    @property
    def data_paths(self):
        """
        Returns an iterator which gives each directory named 'resource' in the application data search path.

        Information provided by earlier directories should take precedence over later ones.

        :return: preference-ordered set of base directories to search for data files directory for ``resource``
        :rtype: list
        """
        tmp_list = [self.data_path]
        for data_dir in self.xdg_data_dirs.split(":"):
            if os.path.exists(os.path.join(data_dir, self.resource)):
                if os.path.join(data_dir, self.resource) not in tmp_list:
                    tmp_list.append(os.path.join(data_dir, self.resource))
        return tmp_list

    @property
    def cache_path(self):
        """
        Ensure ``$XDG_CACHE_HOME/<resource>/`` exists, and return its path.

        :return: ``$XDG_CACHE_HOME/<resource>/`` path
        :rtype: str
        """
        return control_directory(os.path.join(self.xdg_cache_home, self.resource))
