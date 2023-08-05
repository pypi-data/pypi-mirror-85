class GLXShellPropertyCommands(object):
    def __init__(self):
        self.__commands = None
        self.commands = None

    @property
    def commands(self):
        """
        ``commands`` property store the commands list and assure to set commands value only if have changed

        each item should have it dict form: {"name": "Hello", "object": object}

        :return: the commands property value
        :rtype: list or None
        """
        return self.__commands

    @commands.setter
    def commands(self, value=None):
        """
        Set ``commands`` property value

        :param value: a commands list or None
        :type value: list or None
        :raise TypeError: when property value is not a list or None
        """
        if value is None:
            value = []
        if type(value) != list:
            raise TypeError("'commands' property value must be a list or None")
        if self.commands != value:
            self.__commands = value
