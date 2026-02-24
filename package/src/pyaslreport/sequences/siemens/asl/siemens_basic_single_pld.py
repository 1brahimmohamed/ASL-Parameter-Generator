from pyaslreport.sequences.siemens.siemens_base import SiemensBaseSequence
from pyaslreport.utils import dicom_tags_utils as dcm_tags

class SiemensBasicSinglePLD(SiemensBaseSequence):
    @classmethod
    def matches(cls, dicom_header):
        return cls.is_siemens_manufacturer(dicom_header)
        
    @classmethod
    def get_specificity_score(cls) -> int:
        """Lower specificity score because it only checks for manufacturer."""
        return 1

    def extract_bids_metadata(self):
        bids = self._extract_common_metadata()
        bids.update(self._extract_siemens_common_metadata())
        d = self.dicom_header
        if dcm_tags.GE_LABEL_DURATION in d:
            bids["LabelingDuration"] = d.get(dcm_tags.GE_LABEL_DURATION, None).value
        if dcm_tags.GE_INVERSION_TIME in d:
            bids["PostLabelingDelay"] = d.get(dcm_tags.GE_INVERSION_TIME, None).value

        asl_context = self._generate_asl_context(1)
        return bids, asl_context

    def _generate_asl_context(self, npld: int) -> list:
        """
        Generate ASLContext for Siemens sequences.
        For single-PLD: one deltaM volume followed by one m0scan.

        Args:
            npld: Number of post-labeling delays

        Returns:
            list: ASLContext array
        """
        if npld == 1:
            return ["deltaM", "m0scan"]
        else:
            return ["deltaM"] * (npld - 1) + ["m0scan"]