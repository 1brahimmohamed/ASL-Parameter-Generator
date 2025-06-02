from abc import ABC, abstractmethod

class BaseConverter(ABC):
    @abstractmethod
    def convert(self, input_path: str, output_path: str):
        """
        Convert from one format to another.
        Must be implemented by all converters.
        """
        pass
