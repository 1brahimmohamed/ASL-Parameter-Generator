from abc import ABC, abstractmethod

import pydicom


class DSCSequenceBase(ABC):
    def __init__(self, dicom_header: pydicom.Dataset):
        self.dicom_header = dicom_header

    @classmethod
    def matches(cls, dicom_header: pydicom.Dataset) -> bool:
        """Return True if this class can handle the given DICOM header."""
        return True
        

    def extract_bids_metadata(self) -> dict:
        """Extract and convert DICOM metadata to BIDS fields."""

        print('processing DSC sequence')
        
        return {
            "dsc": "dsc params"
        }