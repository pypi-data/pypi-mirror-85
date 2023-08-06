from GLXShell.plugins.builtins import GLXShPluginBuiltins
from GLXShell.plugins.builtins import PLUGIN_VERSION


class GLXShPropertyPlugins(object):
    def __init__(self):
        self.__plugins = None
        self.plugins = None

    @property
    def plugins(self):
        """
        ``plugins`` property store the plugins list and assure to set plugins value only if have changed

        each item should have it dict form: {"name": "Hello", "object": object}

        :return: the plugins property value
        :rtype: list or None
        """
        return self.__plugins

    @plugins.setter
    def plugins(self, value=None):
        """
        Set ``plugins`` property value

        :param value: a plugins list or None
        :type value: list or None
        :raise TypeError: when property value is not a list or None
        """
        if value is None:
            value = [
                {
                    "name": "builtins",
                    "version": PLUGIN_VERSION,
                    "object": GLXShPluginBuiltins(),
                }
            ]
        if type(value) != list:
            raise TypeError("'commands' property value must be a list or None")
        if self.plugins != value:
            self.__plugins = value
