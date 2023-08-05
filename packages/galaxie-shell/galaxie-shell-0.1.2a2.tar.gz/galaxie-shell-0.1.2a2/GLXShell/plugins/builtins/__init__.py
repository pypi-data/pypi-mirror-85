PLUGIN_VERSION = "0.2a"
PLUGIN_NAME = "builtins"
PLUGIN_DESCRIPTION = "glxsh builtins plugin"
PLUGIN_LICENSE = "GNU General Public License v3 or later (GPLv3+)"
PLUGIN_WARRANTY = """Copyright (C) 2020 Galaxie Shell Project.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
"""

from GLXShell.libs.commands import GLXShellCommands
from GLXShell.plugins.builtins.arch import GLXArch
from GLXShell.plugins.builtins.cat import GLXCat
from GLXShell.plugins.builtins.cd import GLXCd
from GLXShell.plugins.builtins.dir import GLXDir
from GLXShell.plugins.builtins.mkdir import GLXMkdir
from GLXShell.plugins.builtins.pwd import GLXPwd
from GLXShell.plugins.builtins.rmdir import GLXRmDir
from GLXShell.plugins.builtins.uname import GLXUname
from GLXShell.plugins.builtins.which import GLXWhich


class GLXShPluginBuiltins(GLXShellCommands):
    def __init__(self):
        GLXShellCommands.__init__(self)
        self.commands = [
            {"name": "arch", "object": GLXArch()},
            {"name": "cat", "object": GLXCat()},
            {"name": "cd", "object": GLXCd()},
            {"name": "dir", "object": GLXDir()},
            {"name": "mkdir", "object": GLXMkdir()},
            {"name": "pwd", "object": GLXPwd()},
            {"name": "rmdir", "object": GLXRmDir()},
            {"name": "uname", "object": GLXUname()},
            {"name": "which", "object": GLXWhich()},
        ]
