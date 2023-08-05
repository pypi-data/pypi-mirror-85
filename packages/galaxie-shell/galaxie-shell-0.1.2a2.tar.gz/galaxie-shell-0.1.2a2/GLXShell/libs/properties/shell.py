class GLXShPropertyShell(object):
    def __init__(self):
        self.__shell = None
        self.shell = None

    @property
    def shell(self):
        """
        ``shell`` property store the shell object and assure to set shell value only if have changed

        :return: a Galaxie Shell instance or None
        :rtype: GLXShell.Shell or None
        """
        return self.__shell

    @shell.setter
    def shell(self, value=None):
        """
        Set ``shell`` property value

        :param value: a Galaxie Shell instance or None
        :type value: GLXShell.Shell or None
        :raise TypeError: when property value is not a Galaxie Shell instance or None
        """
        # if value is None:
        #     value = self
        # if value is not None and not isinstance(value, GLXShell()):
        #     raise TypeError("'shell' property value must be a Galaxie Shell instance or None")
        if self.shell != value:
            self.__shell = value
