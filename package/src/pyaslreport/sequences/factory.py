from pyaslreport.enums.modaliy_enum import ModalityTypeValues
from pyaslreport.sequences.asl.ge import GEBasicSinglePLD, GEMultiPLD
from pyaslreport.sequences.dsc.base_sequence import DSCSequenceBase
import pydicom

ASL_SEQUENCE_CLASSES = [GEBasicSinglePLD, GEMultiPLD]
DSC_SEQUENCE_CLASSES = [DSCSequenceBase]

def get_sequence(modality: str, dicom_header: pydicom.Dataset):

    match modality:
        case ModalityTypeValues.ASL:
            for cls in ASL_SEQUENCE_CLASSES:
                if cls.matches(dicom_header):
                    return cls(dicom_header)
        case ModalityTypeValues.DSC:
            for cls in DSC_SEQUENCE_CLASSES:
                if cls.matches(dicom_header):
                    return cls(dicom_header)
        case _:
            raise ValueError(f"Unsupported modality: {modality}")