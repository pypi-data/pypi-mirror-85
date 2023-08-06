import cmd2

from GLXShell.libs.properties.commands import GLXShellPropertyCommands


class GLXShellCommands(GLXShellPropertyCommands):
    """
    It class have responsibility to receive heritage from ``GLXShPropertyShell`` and ``GLXShellPropertyCommands``.

    Then the class provide ``GLXShellCommands.load()``, ``GLXShellCommands.unload()`` and ``GLXShellCommands.reload()``
    method's.

    It class is include by every plugins, for add method's use directly by the Plugins Manager.
    """

    def __init__(self):
        GLXShellPropertyCommands.__init__(self)

    def load(self):
        """
        It function provide load plugin capability to class it receive heritage from it class.

        ``shell`` property is require and should not be to None, that is done automatically by ``GLXSHell``
        """
        if (
            hasattr(self, "commands")
            and self.commands
            and hasattr(self, "shell")
            and self.shell
        ):
            for command in self.commands:
                try:
                    self.shell.register_command_set(command["object"])
                    if self.shell.debug:
                        self.shell.pwarning("LOAD COMMAND: {0}".format(command["name"]))
                except cmd2.CommandSetRegistrationError:
                    if self.shell.debug:
                        self.shell.perror(
                            "ALREADY LOADED COMMAND: {0}  ".format(command["name"])
                        )

    def unload(self):
        """
        It function provide unload plugin capability to class it receive heritage from it class.

        ``shell`` property is require and should not be to None, that is done automatically by ``GLXSHell``
        """
        if (
            hasattr(self, "commands")
            and self.commands
            and hasattr(self, "shell")
            and self.shell
        ):
            for command in self.commands:
                self.shell.unregister_command_set(command["object"])
                if self.shell.debug:
                    self.shell.pwarning("UNLOAD COMMAND: {0}".format(command["name"]))

    def reload(self):
        """
        It function provide reload plugin capability to class it receive heritage from it class.

        ``shell`` property is require and should not be to None, that is done automatically by ``GLXSHell``
        """
        self.unload()
        self.load()
