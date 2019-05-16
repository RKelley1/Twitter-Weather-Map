from abc import ABCMeta
from abc import abstractmethod


PATH_SEPARATOR = '/'


class ResourceAbstract(object, metaclass=ABCMeta):
    """
    Base resource class. All resources should extend this class

    """
    def __init__(self, root_path=None):
        self.root_path = root_path or (PATH_SEPARATOR + self.get_type())

    @abstractmethod
    def get_type(self):
        raise NotImplementedError
