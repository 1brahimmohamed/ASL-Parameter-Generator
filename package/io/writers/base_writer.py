from abc import ABC, abstractmethod

class BaseWriter(ABC):
    @abstractmethod
    def write(self, data, output_path: str):
        """
        Write the given data to the output path.
        """
        pass
