from GLXShell.libs.plugins import GLXShPluginsManager


class GLXShellPropertyPluginsManager(object):
    def __init__(self):
        self.__plugins_manager = None
        self.plugins_manager = None

    @property
    def plugins_manager(self):
        """
        ``plugins_manager`` property store the plugins_manager object and assure to set plugins_manager value only if
         have changed

        :return: a Galaxie Plugins Manager instance or None
        :rtype: GLXShPluginsManager or None
        """
        return self.__plugins_manager

    @plugins_manager.setter
    def plugins_manager(self, value=None):
        """
        Set ``plugins_manager`` property value

        :param value: a Galaxie Plugins Manager instance or None
        :type value: GLXShPluginsManager or None
        :raise TypeError: when property value is not a Galaxie Plugins Manager instance or None
        """
        if value is None:
            value = GLXShPluginsManager(shell=self)
        if value is not None and not isinstance(value, GLXShPluginsManager):
            raise TypeError(
                "'plugins_manager' property value must be a Galaxie Plugins Manager instance or None"
            )
        if self.plugins_manager != value:
            self.__plugins_manager = value
