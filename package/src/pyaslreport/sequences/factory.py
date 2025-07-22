from pyaslreport.enums.modaliy_enum import ModalityTypeValues
from pyaslreport.sequences.asl.ge import GEBasicSinglePLD, GEMultiPLD
from pyaslreport.sequences.dsc.base_sequence import DSCSequenceBase
import pydicom

ASL_SEQUENCE_CLASSES = [GEBasicSinglePLD, GEMultiPLD]
DSC_SEQUENCE_CLASSES = [DSCSequenceBase]

def get_sequence(modality: str, dicom_header: pydicom.Dataset):
    match modality:
        case ModalityTypeValues.ASL:
            # Sort by specificity - more specific matchers first
            sorted_classes = sorted(
                ASL_SEQUENCE_CLASSES,
                key=lambda cls: cls.get_specificity_score() if hasattr(cls, 'get_specificity_score') else 0,
                reverse=True
            )
            for cls in sorted_classes:
                if cls.matches(dicom_header):
                    print(f"Matched ASL sequence class: {cls.__name__}")
                    return cls(dicom_header)
            
            raise ValueError(f"No ASL sequence class found that matches the DICOM header")
        case ModalityTypeValues.DSC:
            for cls in DSC_SEQUENCE_CLASSES:
                if cls.matches(dicom_header):
                    print(f"Matched DSC sequence class: {cls.__name__}")
                    return cls(dicom_header)
            
            raise ValueError(f"No DSC sequence class found that matches the DICOM header")
        case _:
            raise ValueError(f"Unsupported modality: {modality}")