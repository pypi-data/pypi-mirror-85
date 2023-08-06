import os
import cmd2


from GLXShell.plugins.builtins import PLUGIN_VERSION
from GLXShell.plugins.builtins import PLUGIN_DESCRIPTION
from GLXShell.plugins.builtins import PLUGIN_WARRANTY

# Inspired from: http://pwet.fr/man/linux/commandes/posix/cd/


cd_parser = cmd2.Cmd2ArgumentParser(
    prog="CD",
    description="Change the working directory",
)

cd_parser.add_argument(
    "directory",
    nargs="?",
    const=0,
    help="An absolute or relative pathname of the directory that shall become the new working directory.",
)
cd_parser.add_argument(
    "-P",
    "--physical",
    action="store_true",
    default=False,
    help="Symbolic link components shall be resolved before dot-dot components are processed",
)
cd_parser.add_argument(
    "-L",
    "--logical",
    action="store_true",
    default=False,
    help="Symbolic link components shall not be resolved before dot-dot components are processed",
)
cd_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)


class GLXCd(cmd2.CommandSet):
    def __init__(self):
        super().__init__()
        self.__curpath = None
        self.__directory = None
        self.__logical = None
        self.__physical = None
        self.__can_continue = None

        self.curpath = None
        self.directory = None
        self.logical = None
        self.physical = None
        self.can_continue = None

    @property
    def curpath(self):
        """
        ``curpath`` represents an intermediate value used to simplify the description of the algorithm used by cd.

        :return: value used to simplify the description
        :rtype: str or None
        """
        return self.__curpath

    @curpath.setter
    def curpath(self, value=None):
        """
        Set the ``curpath`` property value

        :param value: value used to simplify the description
        :type value: str or None
        :raise TypeError: when ``directory`` property value is not str type or None
        """
        if value is not None and type(value) != str:
            raise TypeError("'curpath' property value must be str type or None")
        if self.curpath != value:
            self.__curpath = value

    @property
    def directory(self):
        """
        An absolute or relative pathname of the directory that shall become the new working directory.

        :return: directory that shall become the new working directory
        :rtype: str or None
        """
        return self.__directory

    @directory.setter
    def directory(self, value=None):
        """
        Set the ``directory`` property value

        :param value: directory that shall become the new working directory
        :type value: str or None
        :raise TypeError: when ``directory`` property value is not str type or None
        """
        if value is not None and type(value) != str:
            raise TypeError("'directory' property value must be str type or None")
        if self.directory != value:
            self.__directory = value

    @property
    def logical(self):
        """
        The ``logical`` property is use as control during the 9 steps of the posix sequence

        Default: False

        :return: True if handle the operand dot-dot logically
        :rtype: bool
        """
        return self.__logical

    @logical.setter
    def logical(self, value=None):
        """
        Set the ``logical`` property value

        Default: False

        :param value: True if handle the operand dot-dot logically
        :type value: bool or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError("'logical' property value must be bool type or None")
        if self.logical != value:
            self.__logical = value

    @property
    def physical(self):
        """
        The ``physical`` property is use as control during the 9 steps of the posix sequence

        Default: False

        :return: True if handle the operand dot-dot physically
        :rtype: bool
        """
        return self.__physical

    @physical.setter
    def physical(self, value=None):
        """
        Set the ``physical`` property value

        Default: True

        :param value: True if handle the operand dot-dot physically
        :type value: bool or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError("'physical' property value must be bool type or None")
        if self.physical != value:
            self.__physical = value

    @property
    def can_continue(self):
        """
        The ``working`` property is use as control during the 9 steps of the posix sequence

        Default: True

        :return: True if any step can be operate
        :rtype: bool
        """
        return self.__can_continue

    @can_continue.setter
    def can_continue(self, value=None):
        """
        Set the ``working`` property value

        Default: True

        :param value: True if any step can be operate
        :type value: bool or None
        """
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'working' property value must be bool type or None")
        if self.can_continue != value:
            self.__can_continue = value

    @staticmethod
    def cd_print_version():
        cmd2.Cmd().poutput(
            "cd ({name}) v{version}\n{licence}".format(
                name=PLUGIN_DESCRIPTION,
                version=PLUGIN_VERSION,
                licence=PLUGIN_WARRANTY,
            )
        )

    def cd(self, directory=None, logical=None, physical=None):
        # Init
        self.can_continue = True
        self.curpath = None

        self.directory = directory
        self.logical = logical
        self.physical = physical

        # Logical
        if self.logical and self.physical:
            self.physical = False
        if not self.logical and not self.physical:
            self.logical = True

        if self.directory == "-":
            if os.environ.get("OLDPWD"):
                self.directory = os.environ.get("OLDPWD")
            else:
                self.directory = os.environ.get("PWD")

        elif self.directory is not None:
            self.directory = os.path.expanduser(self.directory)

        # Start the posix sequence
        self._step_1()
        self._step_2()
        self._step_3()
        self._step_4()
        self._step_5()
        self._step_6()
        self._step_7()
        self._step_8()
        self._step_9()

        # Inform cmd2 directly
        cmd2.Cmd().last_result = os.getcwd()
        cmd2.Cmd().set_window_title(
            os.path.normpath(os.getcwd()).replace(
                os.path.realpath(os.path.expanduser("~")), "~"
            )
        )

    def _step_1(self):
        """
        If no directory operand is given and the HOME environment variable is empty or undefined,
        the default behavior is implementation-defined and no further steps shall be taken.
        """
        if self.can_continue and self.directory is None and not os.environ.get("HOME"):
            self.can_continue = False

    def _step_2(self):
        """
        If no directory operand is given and the HOME environment variable is set to a non-empty value,
        the *cd* utility shall behave as if the directory named in the HOME environment variable was
        specified as the directory operand.
        """
        if self.can_continue and self.directory is None and os.environ.get("HOME"):
            self.directory = os.environ.get("HOME")

    def _step_3(self):
        """
        If the directory operand begins with a slash character, set ``curpath`` to the operand and proceed to step 7.
        """
        if self.can_continue and self.directory.startswith(os.path.sep):
            self.curpath = self.directory
            self._step_7()

    def _step_4(self):
        """
        If the first component of the directory operand is dot or dot-dot, proceed to step 6.
        """
        if (
            self.can_continue
            and self.directory.startswith("..")
            or self.directory.startswith(".")
        ):
            self._step_6()

    def _step_5(self):
        """
        Starting with the first pathname in the colon-separated pathnames of CDPATH
        (see the ENVIRONMENT VARIABLES section) if the pathname is non-null,
        test if the concatenation of that pathname, a slash character, and the directory operand names a directory.

        If the pathname is null, test if the concatenation of dot, a slash character, and the operand names a directory.

        In either case, if the resulting string names an existing directory,
        set curpath to that string and proceed to step 7.

        Otherwise, repeat this step with the next pathname in CDPATH until all pathnames have been tested.
        """
        # 5. Starting with the first pathname in the colon-separated pathnames of CDPATH
        # (see the ENVIRONMENT VARIABLES section)
        if self.can_continue and os.environ.get("CDPATH"):
            for pathname in os.environ.get("CDPATH").split(":"):
                if pathname:
                    # if the pathname is non-null, test if the concatenation of that pathname,
                    # a slash character, and the directory operand names a directory.
                    if os.path.isdir(os.path.join(pathname, self.directory)):
                        self.curpath = os.path.join(pathname, self.directory)
                        self._step_7()
                        break
                    # If the pathname is null, test if the concatenation of dot, a slash character, and
                    # the operand names a directory.
                    # set curpath to that string and proceed to step 7.
                    elif os.path.isdir(
                        os.path.join(".{0}".format(os.path.sep), self.directory)
                    ):
                        self.curpath = os.path.join(
                            ".{0}".format(os.path.sep), self.directory
                        )
                        self._step_7()
                        break
                    # elif os.path.isdir(pathname):
                    #     # In either case, if the resulting string names an existing directory,
                    #     self.curpath = pathname
                    #     self._step_7()
                    #     break

                # Otherwise, repeat this step with the next pathname in CDPATH until all pathnames have been tested.

    def _step_6(self):
        """
        Set ``curpath`` to the string formed by the concatenation of the value of *PWD* , a slash character,
        and the operand.
        """
        if self.can_continue:
            self.curpath = os.path.join(os.environ.get("PWD"), self.directory)

    def _step_7(self):
        """
        If the **-P** option is in effect, the cd utility shall perform actions equivalent to the chdir() function,
         called with ``curpath`` as the path argument.

        If these actions succeed, the *PWD* environment variable shall be set to an absolute pathname for
        the current working directory and shall not contain filename components that,
        in the context of pathname resolution, refer to a file of type symbolic link.

        If there is insufficient permission on the new directory, or on any parent of that directory,
        to determine the current working directory, the value of the *PWD* environment variable is unspecified.

        If the actions equivalent to ``chdir()`` fail for any reason, the cd utility shall display
        an appropriate error message and not alter the PWD environment variable.

        Whether the actions equivalent to ``chdir()`` succeed or fail, no further steps shall be taken.
        """
        if self.can_continue and self.physical:
            # Make sure the directory exists, is a directory, and we have read access
            err = None

            if not os.path.isdir(self.curpath):
                err = f"cd: {self.curpath}: No such file or directory"
            elif not os.access(self.curpath, os.R_OK):  # pragma: no cover
                err = f"cd: {self.curpath}: Permission denied"
            else:
                try:
                    os.chdir(self.curpath)
                except Exception as ex:  # pragma: no cover
                    err = f"{ex}"
                else:
                    if os.environ.get("OLDPWD") != os.environ["PWD"]:
                        os.environ["OLDPWD"] = os.environ["PWD"]
                    if os.environ["PWD"] != os.path.normpath(os.getcwd()):
                        os.environ["PWD"] = os.path.normpath(os.getcwd())

            if err:
                cmd2.Cmd().perror(err)

            self.can_continue = False

    def _step_8(self):
        """
        The ``curpath`` value shall then be converted to canonical form as follows, considering each component
        from beginning to end, in sequence:

        a. Dot components and any slashes that separate them from the next component shall be deleted.

        b. For each dot-dot component, if there is a preceding component and it is neither root nor dot-dot,
        the preceding component, all slashes separating the preceding component from dot-dot, dot-dot and all slashes
        separating dot-dot from the following component shall be deleted.

        c. An implementation may further simplify ``curpath`` by removing any trailing slash characters that are not
        also leading slashes, replacing multiple non-leading consecutive slashes with a single slash, and replacing
        three or more leading slashes with a single slash. If, as a result of this canonicalization, the ``curpath``
        variable is null, no further steps shall be taken.
        """
        if self.can_continue:
            self.curpath = os.path.abspath(self.curpath)

    def _step_9(self):
        """
        The cd utility shall then perform actions equivalent to the ``chdir()`` function called with ``curpath`` as
        the path argument.

        If these actions failed for any reason, the cd utility shall display an appropriate error message
        and no further steps shall be taken.

        The *PWD* environment variable shall be set to ``curpath``.
        """
        if self.can_continue:
            err = None

            if not os.path.isdir(self.curpath):
                err = f"cd: {self.curpath}: No such file or directory"
            elif not os.access(self.curpath, os.R_OK):  # pragma: no cover
                err = f"cd: {self.curpath}: Permission denied"
            else:
                try:
                    os.chdir(self.curpath)
                except Exception as ex:  # pragma: no cover
                    err = f"{ex}"
                else:
                    if os.environ.get("OLDPWD") != os.environ["PWD"]:
                        os.environ["OLDPWD"] = os.environ["PWD"]
                    if os.environ["PWD"] != self.curpath:
                        os.environ["PWD"] = self.curpath

            if err:
                cmd2.Cmd().perror(err)
            self.can_continue = False

    @cmd2.with_argparser(cd_parser)
    @cmd2.with_category("Builtins")
    def do_cd(self, args):
        if args.version:  # pragma: no cover
            self.cd_print_version()
            return

        self.cd(
            directory=args.directory, logical=args.logical, physical=args.physical
        )  # pragma: no cover

    @staticmethod
    def complete_cd(text, line, begidx, endidx):
        return cmd2.Cmd().path_complete(
            text=text,
            line=line,
            begidx=begidx,
            endidx=endidx,
            path_filter=os.path.isdir,
        )
