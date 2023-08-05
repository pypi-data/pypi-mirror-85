import cmd2
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    Union,
)

from GLXShell.libs.properties.shortcuts import GLXShPropertyShortcuts
from GLXShell.libs.properties.history import GLXShPropertyHistory
from GLXShell.libs.properties.config import GLXShPropertyConfig
from GLXShell.libs.properties.shell import GLXShPropertyShell


from GLXShell.libs.plugins import GLXShPluginsManager
from GLXShell.libs.intro import GLXShIntro
from GLXShell.libs.prompt import GLXShPrompt
from GLXShell.libs.settable import GLXShSettable


# Key binding
# http://readline.kablamo.org/emacs.html


class GLXShell(
    GLXShPropertyShortcuts,
    GLXShPropertyHistory,
    GLXShPropertyConfig,
    GLXShPropertyShell,
    GLXShPluginsManager,
    GLXShIntro,
    GLXShPrompt,
    cmd2.Cmd,
    GLXShSettable,
):
    """An easy but powerful survival kit for writing line-oriented command interpreters.

    Extends the Python Standard Library’s cmd2 package by adding a lot of useful features
    to the out of the box configuration.

    Line-oriented command interpreters are often useful for test harnesses, internal tools, and rapid prototypes.

    :param completekey: readline name of a completion key, default to Tab
    :param stdin: alternate input file object, if not specified, sys.stdin is used
    :param stdout: alternate output file object, if not specified, sys.stdout is used
    :param persistent_history_file: file path to load a persistent cmd2 command history from
    :param persistent_history_length: max number of history items to write
                                      to the persistent history file
    :param startup_script: file path to a script to execute at startup
    :param use_ipython: should the "ipy" command be included for an embedded IPython shell
    :param allow_cli_args: if ``True``, then :meth:`cmd2.Cmd.__init__` will process command
                           line arguments as either commands to be run or, if ``-t`` or
                           ``--test`` are given, transcript files to run. This should be
                           set to ``False`` if your application parses its own command line
                           arguments.
    :param transcript_files: pass a list of transcript files to be run on initialization.
                             This allows running transcript tests when ``allow_cli_args``
                             is ``False``. If ``allow_cli_args`` is ``True`` this parameter
                             is ignored.
    :param allow_redirection: If ``False``, prevent output redirection and piping to shell
                              commands. This parameter prevents redirection and piping, but
                              does not alter parsing behavior. A user can still type
                              redirection and piping tokens, and they will be parsed as such
                              but they won't do anything.
    :param multiline_commands: list of commands allowed to accept multi-line input
    :param terminators: list of characters that terminate a command. These are mainly
                        intended for terminating multiline commands, but will also
                        terminate single-line commands. If not supplied, the default
                        is a semicolon. If your app only contains single-line commands
                        and you want terminators to be treated as literals by the parser,
                        then set this to an empty list.
    :param shortcuts: dictionary containing shortcuts for commands. If not supplied,
                      then defaults to constants.DEFAULT_SHORTCUTS. If you do not want
                      any shortcuts, pass an empty dictionary.
    :param command_sets: Provide CommandSet instances to load during cmd2 initialization.
                         This allows CommandSets with custom constructor parameters to be
                         loaded.  This also allows the a set of CommandSets to be provided
                         when `auto_load_commands` is set to False
    :param auto_load_commands: If True, cmd2 will check for all subclasses of `CommandSet`
                               that are currently loaded by Python and automatically
                               instantiate and register all commands. If False, CommandSets
                               must be manually installed with `register_command_set`.
    :param auto_load_plugins: If True, plugins will be load at end of the init
    :param auto_load_settable: If True, settable will be load at end of the init
    :param default_to_shell: If True, unknowns commands will be sed to the sub system
    """

    def __init__(
        self,
        completekey: str = "tab",
        stdin=None,
        stdout=None,
        *,
        persistent_history_file: str = "",
        persistent_history_length: int = 1000,
        startup_script: str = "",
        use_ipython: bool = False,
        allow_cli_args: bool = True,
        transcript_files: Optional[List[str]] = None,
        allow_redirection: bool = True,
        multiline_commands: Optional[List[str]] = None,
        terminators: Optional[List[str]] = None,
        shortcuts: Optional[Dict[str, str]] = None,
        command_sets: Optional[Iterable[cmd2.CommandSet]] = None,
        auto_load_commands: bool = False,
        auto_load_plugins: bool = True,
        auto_load_settable: bool = True,
        default_to_shell: bool = True,
        debug: bool = False,
    ) -> None:
        GLXShPropertyShortcuts.__init__(self)
        GLXShPropertyHistory.__init__(self)
        GLXShPropertyShell.__init__(self)
        GLXShPropertyConfig.__init__(self)

        self.shell = self

        GLXShIntro.__init__(self)
        GLXShPrompt.__init__(self)
        GLXShPluginsManager.__init__(self)

        self.persistent_history_file = persistent_history_file
        self.persistent_history_length = persistent_history_length
        self.shortcuts = shortcuts

        # Init and config the cmd2 object
        cmd2.Cmd.__init__(
            self,
            completekey=completekey,
            stdin=stdin,
            stdout=stdout,
            persistent_history_file=self.persistent_history_file,
            persistent_history_length=self.persistent_history_length,
            startup_script=startup_script,
            use_ipython=use_ipython,
            allow_cli_args=allow_cli_args,
            transcript_files=transcript_files,
            allow_redirection=allow_redirection,
            multiline_commands=multiline_commands,
            terminators=terminators,
            shortcuts=self.shortcuts,
            command_sets=command_sets,
            auto_load_commands=auto_load_commands,
        )
        self.debug = debug
        self.default_to_shell = default_to_shell
        self.auto_load_settable = auto_load_settable
        self.auto_load_plugins = auto_load_plugins
        # PostProcessing
        if self.auto_load_plugins:
            self.plugins_manager_control_config()
            self.load_plugins()
        if self.auto_load_settable:
            GLXShSettable(self).load_settable()

    @property
    def intro(self):
        """
        Return intro to displays, it property is call one time at startup by ``cmd2`` python module
        """
        return self.intro_to_display

    @property
    def prompt(self):
        """
        Return prompt to displays, the prompt is display just before the blinking cursor on the terminal
        """
        return self.prompt_to_display
