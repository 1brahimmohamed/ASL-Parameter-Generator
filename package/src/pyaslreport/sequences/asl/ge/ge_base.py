from pyaslreport.sequences.asl.base_sequence import ASLSequenceBase

class GEBaseSequence(ASLSequenceBase):
    def _extract_ge_common_metadata(self) -> dict:
        d = self.dicom_header
        bids = {}
        # Direct GE-specific mappings
        if "AssetRFactor" in d:
            bids["AssetRFactor"] = d.get("AssetRFactor", None)
        if "EffectiveEchoSpacing" in d:
            bids["EffectiveEchoSpacing"] = d.get("EffectiveEchoSpacing", None)
        if "AcquisitionMatrix" in d:
            bids["AcquisitionMatrix"] = d.get("AcquisitionMatrix", None)
        if "NumberOfExcitations" in d:
            bids["TotalAcquiredPairs"] = d.get("NumberOfExcitations", None)
            
        # Derived fields
        # EffectiveEchoSpacing = EffectiveEchoSpacing * AssetRFactor * 1e-6
        if "EffectiveEchoSpacing" in d and "AssetRFactor" in d:
            try:
                eff_echo = float(d.get("EffectiveEchoSpacing", None))
                asset = float(d.get("AssetRFactor", None))
                bids["EffectiveEchoSpacing"] = eff_echo * asset * 1e-6
            except Exception:
                pass

        # TotalReadoutTime = (AcquisitionMatrix[0] - 1) * EffectiveEchoSpacing
        if (
            "AcquisitionMatrix" in d and
            isinstance(d.get("AcquisitionMatrix", None), (list, tuple)) and
            len(d.get("AcquisitionMatrix", None)) > 0 and
            "EffectiveEchoSpacing" in bids
        ):
            try:
                acq_matrix = d.get("AcquisitionMatrix", None)[0]
                eff_echo = bids["EffectiveEchoSpacing"]
                bids["TotalReadoutTime"] = (acq_matrix - 1) * eff_echo
            except Exception:
                pass
        
        # MRAcquisitionType default is 3D if not present
        if "MRAcquisitionType" in d:
            bids["MRAcquisitionType"] = d.get("MRAcquisitionType", None)
        else:
            bids["MRAcquisitionType"] = "3D"

        # PulseSequenceType default is spiral if not present
        if "PulseSequenceType" in d:
            bids["PulseSequenceType"] = d.get("PulseSequenceType", None)
        else:
            bids["PulseSequenceType"] = "spiral"

        return bids
