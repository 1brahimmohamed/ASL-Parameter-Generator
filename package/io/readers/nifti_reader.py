import nibabel as nib
from package.core.exceptions import ReaderError
from package.core.logging import get_logger
from .base_reader import BaseReader

logger = get_logger(__name__)

class NiftiReader(BaseReader):

    def __init__(self):
        logger.debug("Initialized NIfTIReader")

    def read(self, nifti_file_path: str):
        """
        Read NIfTI data from the input path and return it in a standardized format.
        Args:
            nifti_file_path (str): Path to the NIfTI file (.nii or .nii.gz)
        Returns:
            Nifti Image (nib.Nifti1Image): Loaded NIfTI image object
        """
        if not isinstance(nifti_file_path, str) or not nifti_file_path.endswith(('.nii', '.nii.gz')):
            raise ReaderError(f"Invalid NIfTI file path: {nifti_file_path}")

        try:
            return nib.load(nifti_file_path)
        except Exception as e:
            logger.error(f"Failed to read NIfTI file {nifti_file_path}: {e}")
            raise ReaderError(f"Failed to read NIfTI file: {e}") from e

