from .ge_base import GEBaseSequence
import math
from pyaslreport.utils import dicom_tags_utils as dcm_tags

class GEMultiPLD(GEBaseSequence):
    @classmethod
    def matches(cls, dicom_header):
        return (
            cls.is_ge_manufacturer(dicom_header) and
            dicom_header.get(dcm_tags.GE_INTERNAL_SEQUENCE_NAME, "").value.strip().lower() == "easl"
        )

    @classmethod
    def get_specificity_score(cls) -> int:
        """Higher specificity score because it checks for specific sequence name."""
        return 10

    def extract_bids_metadata(self):
        bids = self._extract_common_metadata()
        bids.update(self._extract_ge_common_metadata())
        d = self.dicom_header
        # eASL-specific tags
        for dicom_key, bids_key in [
            (dcm_tags.GE_PRIVATE_CV4, "GEPrivateCV4"),
            (dcm_tags.GE_PRIVATE_CV5, "GEPrivateCV5"),
            (dcm_tags.GE_PRIVATE_CV6, "GEPrivateCV6"),
            (dcm_tags.GE_PRIVATE_CV7, "GEPrivateCV7"),
            (dcm_tags.GE_PRIVATE_CV8, "GEPrivateCV8"),
            (dcm_tags.GE_PRIVATE_CV9, "GEPrivateCV9"),
        ]:
            if dicom_key in d:
                bids[bids_key] = d.get(dicom_key, None).value

        # ArterialSpinLabelingType is always 'PCASL'
        bids["ArterialSpinLabelingType"] = "PCASL"

        # Calculate LabelingDuration and PostLabelingDelay arrays
        npld = d.get(dcm_tags.GE_PRIVATE_CV6, None).value
        if npld is not None:
            try:
                npld = int(npld)
            except Exception:
                npld = None
                
        if npld == 1:
            # Single-PLD
            bids["LabelingDuration"] = d.get(dcm_tags.GE_PRIVATE_CV5, None).value
            bids["PostLabelingDelay"] = d.get(dcm_tags.GE_PRIVATE_CV4, None).value
        elif npld and npld > 1:
            # Multi-PLD
            cv4 = float(d.get(dcm_tags.GE_PRIVATE_CV4, 0).value)
            cv5 = float(d.get(dcm_tags.GE_PRIVATE_CV5, 0).value)
            cv7 = float(d.get(dcm_tags.GE_PRIVATE_CV7, 1).value)
            magnetic_field_strength = float(d.get(dcm_tags.MAGNETIC_FIELD_STRENGTH, 3).value)
            
            # T1 for blood
            T1 = 1.65 if magnetic_field_strength == 3 else 1.4
            LD_lin = [cv5 / npld] * npld
            PLD_lin = [cv4 + i * LD_lin[0] for i in range(npld)]
            LD_exp = []
            PLD_exp = [cv4]
            Starget = npld * (1 - math.exp(-cv5 / T1)) * math.exp(-cv4 / T1)
            # for i in range(npld):
            #     if i == 0:
            #         LD_exp.append(-T1 * math.log(1 - Starget * math.exp(PLD_exp[0] / T1)))
            #     else:
            #         PLD_exp.append(PLD_exp[i-1] + LD_exp[i-1])
            #         LD_exp.append(-T1 * math.log(1 - Starget * math.exp(PLD_exp[i] / T1)))
            if cv7 == 1:
                bids["LabelingDuration"] = LD_lin
                bids["PostLabelingDelay"] = PLD_lin
            elif cv7 == 0:
                bids["LabelingDuration"] = LD_exp
                bids["PostLabelingDelay"] = PLD_exp
            else:
                # Linear combination
                bids["LabelingDuration"] = [ld_lin * cv7 + ld_exp * (1 - cv7) for ld_lin, ld_exp in zip(LD_lin, LD_exp)]
                bids["PostLabelingDelay"] = [pld_lin * cv7 + pld_exp * (1 - cv7) for pld_lin, pld_exp in zip(PLD_lin, PLD_exp)]
        # ASLcontext: all deltaM, last one is m0scan
        bids["ASLContext"] = ["volume_type"] + ["deltaM"] * (npld - 1) + ["m0scan"] if npld and npld > 1 else ["deltaM", "m0scan"]
        return bids 