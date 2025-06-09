from abc import ABC, abstractmethod

class BaseReader(ABC):
    @abstractmethod
    def read(self, path: str):
        """
        Read data from the input path and return it in a standardized format.
        """
        pass
