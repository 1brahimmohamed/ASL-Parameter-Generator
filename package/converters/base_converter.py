from abc import ABC, abstractmethod

class BaseConverter(ABC):
    @abstractmethod
    def convert(self):
        """
        Convert from one format to another.
        Must be implemented by all converters.
        """
        pass
