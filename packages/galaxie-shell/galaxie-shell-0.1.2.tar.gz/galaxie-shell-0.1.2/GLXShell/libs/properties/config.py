from GLXShell.libs.config import GLXShConfig


class GLXShPropertyConfig(object):
    def __init__(self):
        self.__config = None
        self.config = None

    @property
    def config(self):
        """
        ``config`` property store the config object and assure to set config value only if have changed

        :return: a Galaxie Shell instance or None
        :rtype: GLXShell.Shell or None
        """
        return self.__config

    @config.setter
    def config(self, value=None):
        """
        Set ``config`` property value

        :param value: a Galaxie Shell Config instance or None
        :type value: GLXShConfig or None
        :raise TypeError: when property value is not a Galaxie Shell Config instance or None
        """
        if value is None:
            value = GLXShConfig()
        if value is not None and not isinstance(value, GLXShConfig):
            raise TypeError(
                "'shell' property value must be a Galaxie Shell Config instance or None"
            )
        if self.config != value:
            self.__config = value
