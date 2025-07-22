from operator import truediv
from pyaslreport.sequences.ge.ge_base import GEBaseSequence



class GEASLBase(GEBaseSequence):
    
    def _extract_ge_common_asl_metadata(self):
        d = self.dicom_header
        bids_ge_asl = {}

        bids_ge_asl["BackgroundSuppression"] = True
        bids_ge_asl["BackgroundSuppressionNumberPulses"] = 4
        bids_ge_asl["M0Type"] = "Included"

        return bids_ge_asl
