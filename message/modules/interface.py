from abc import abstractclassmethod, abstractmethod, abstractproperty


class interface:
    """
    Abstract class for all interfaces.
    """
    @abstractclassmethod
    def __init__(self):
        pass

    @abstractclassmethod
    def permission():
        """
        store the permission of the interface.
        """
        pass

    @abstractproperty
    def alia(self):
        """
        alia of the interface.
        """
        pass

    @abstractproperty
    def description(self):
        """
        Description of the interface.
        """
        pass

    @abstractproperty
    def run(self, data):
        """
        use the first message to initialize the interface.
        """
        pass

    @abstractproperty
    def add(self):
        """
        add one message to the interface.
        """
        pass

    @abstractproperty
    def main(self):
        """
        Main function of the interface.
        """
        pass
