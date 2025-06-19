import json
import math
import os
from typing import Any, Dict

from pyaslreport.converters.dicom_to_nifti_converter import DICOM2NiFTIConverter
from pyaslreport.io.readers.nifti_reader import NiftiReader
from pyaslreport.io.writers.json_writer import JSONWriter
from pyaslreport.io.writers.report_writer import ReportWriter
from pyaslreport.modalities.asl.report_generator import ReportGenerator
from pyaslreport.modalities.asl.utils import ASLUtils
from pyaslreport.modalities.asl.validator import ASLValidator
from pyaslreport.modalities.base_processor import BaseProcessor
from pyaslreport.modalities.asl.constants import DURATION_OF_EACH_RFBLOCK
from pyaslreport.utils.general_utils import GeneralUtils
from pyaslreport.utils.unit_conversion_utils import UnitConverterUtils
from pyaslreport.core.config import config


class ASLProcessor(BaseProcessor):
    """
    Class for processing ASL (Arterial Spin Labeling) data.
    This class inherits from BaseProcessor and implements the process method to handle ASL report generation.
    """

    # data here is expected to be an object with attributes `files`, nifti_file`, and `dcm_files`

    def __init__(self, data) -> None:
        """
        Initialize the ASLProcessor with the input data.

        :param data: The input data to be processed.
        """

        # create tmp upload folder if it does not exist
        os.makedirs("/tmp/upload", exist_ok=True)

        super().__init__(data)

    def process(self) -> Dict[str, Any]:

        if (not self.data["files"]) and not self.data["dcm_files"]:
            raise ValueError("No files provided for ASL processing.")

        converted_files, new_filenames, nifti_file, file_format, error = DICOM2NiFTIConverter.convert(
            self.data["dcm_files"], self.data["nifti_file"])

        if converted_files:
            self.data["files"].extend(converted_files)

        if (error == "No DICOM files found.") and (not self.data["files"]):
            raise RuntimeError("Neither DICOM nor NIfTI files were found.")
        elif (error != "No DICOM files found.") and error:
            raise RuntimeError(f"Error during conversion: {error}")

        if converted_files:
            self.data["files"].extend(converted_files)
            self.data['filenames'].extend(new_filenames)

        grouped_files = ASLUtils.group_files(self.data["files"], self.data['filenames'], file_format, "/tmp/upload")

        nifti_slice_number = NiftiReader.read(nifti_file)

        asl_json_filenames, asl_json_data, m0_prep_times_collection = [], [], []
        errors, warnings, all_absent, bs_all_off = [], [], True, True

        for group in grouped_files:
            if group['asl_json'] is not None:
                asl_filename, asl_data_or_path = group['asl_json']
                asl_json_filenames.append(asl_filename)

                # Check if asl_data_or_path is a file path (string) and read the file
                if isinstance(asl_data_or_path, str):
                    with open(asl_data_or_path, 'r') as file:
                        asl_data: Dict[str, Any] = json.load(file)
                else:
                    asl_data = asl_data_or_path
                asl_json_data.append(asl_data)

                m0_type = asl_data.get("M0Type")
                if m0_type != "Absent":
                    all_absent = False
                if asl_data.get("BackgroundSuppression", []):
                    bs_all_off = False

            # Convert all necessary values from seconds to milliseconds before validation

        # Convert all necessary values from seconds to milliseconds before validation
        for session in asl_json_data:
            """
            if 'ScanningSequence' in session:
              session['ScanningSequence'] = session['ScanningSequence']
              del session['ScanningSequence']
            """
            if 'RepetitionTime' in session:
                session['RepetitionTimePreparation'] = session['RepetitionTime']
                del session['RepetitionTime']
            if 'InversionTime' in session:
                session['PostLabelingDelay'] = session['InversionTime']
                del session['InversionTime']
            if 'BolusDuration' in session:
                session['BolusCutOffDelayTime'] = session['BolusDuration']
                del session['BolusDuration']
            if 'NumRFBlocks' in session:
                session['LabelingDuration'] = session['NumRFBlocks'] * DURATION_OF_EACH_RFBLOCK
            if 'InitialPostLabelDelay' in session:
                session['PostLabelingDelay'] = session['InitialPostLabelDelay']
                del session['InitialPostLabelDelay']

            for key in ['EchoTime', 'RepetitionTimePreparation', 'LabelingDuration',
                        'BolusCutOffDelayTime', 'BackgroundSuppressionPulseTime', "PostLabelingDelay"]:
                if key in session:
                    session[key] = UnitConverterUtils.convert_to_milliseconds(session[key])
            session['PLDType'] = ASLUtils.determine_pld_type(session)

        # Clean up upload folder
        # GeneralUtils.clean_up_folder("/tmp/upload")

        m0_type = None
        global_pattern = None
        total_acquired_pairs = None
        for i, group in enumerate(grouped_files):
            if group['asl_json'] is not None:
                asl_filename = asl_json_filenames[i]
                asl_data = asl_json_data[i]
                m0_type = asl_data.get("M0Type")

                if group['m0_json'] is not None:
                    m0_filename, m0_data = group['m0_json']
                    for key in ['EchoTime', 'RepetitionTimePreparation', 'RepetitionTime']:
                        if key in m0_data:
                            m0_data[key] = UnitConverterUtils.convert_to_milliseconds(m0_data[key])
                    if m0_type == "Absent":
                        errors.append(
                            f"Error: M0 type specified as 'Absent' for '{asl_filename}', but"
                            f" '{m0_filename}' is present")
                    elif m0_type == "Included":
                        errors.append(
                            f"Error: M0 type specified as 'Included' for '{asl_filename}', but"
                            f" '{m0_filename}' is present")
                    params_asl, params_m0 = ASLUtils.extract_params(asl_data), ASLUtils.extract_params(m0_data)
                    errors.extend(ASLUtils.compare_params(params_asl, params_m0, asl_filename, m0_filename)[0])
                    warnings.extend(ASLUtils.compare_params(params_asl, params_m0, asl_filename, m0_filename)[1])

                    m0_prep_time = m0_data.get("RepetitionTimePreparation", [])
                    m0_prep_times_collection.append(m0_prep_time)
                else:
                    if m0_type == "Separate":
                        errors.append(
                            f"Error: M0 type specified as 'Separate' for '{asl_filename}', but"
                            f" m0scan.json is not provided.")

                if group['tsv'] is not None:
                    tsv_filename, tsv_data = group['tsv']
                    m0scan_count = sum(1 for line in tsv_data if line.strip() == "m0scan")
                    volume_types = [line.strip() for line in tsv_data if line.strip()]
                    pattern, total_acquired_pairs = ASLUtils.analyze_volume_types(volume_types)
                    asl_data['TotalAcquiredPairs'] = total_acquired_pairs

                    if global_pattern is None:
                        global_pattern = pattern
                    elif global_pattern != pattern:
                        global_pattern = "control-label (there's no consistent control-label or label-control order)"
                    if m0scan_count > 0:
                        if m0_type == "Absent":
                            errors.append(
                                f"Error: m0 type is specified as 'Absent' for '{asl_filename}', but"
                                f" '{tsv_filename}' contains m0scan.")
                        elif m0_type == "Separate":
                            errors.append(
                                f"Error: m0 type is specified as 'Separate' for '{asl_filename}', but"
                                f" '{tsv_filename}' contains m0scan.")
                        else:
                            repetition_times = asl_data.get("RepetitionTimePreparation", [])

                            if not isinstance(repetition_times, list):
                                repetition_times = [repetition_times]
                            repetition_times_max = max(repetition_times)
                            repetition_times_min = min(repetition_times)

                            if len(repetition_times) > m0scan_count:
                                m0_prep_times_collection.append(repetition_times[0])
                                asl_data["RepetitionTimePreparation"] = repetition_times[m0scan_count:]
                            elif (repetition_times_max - repetition_times_min) < 10e-5:
                                m0_prep_times_collection.append(repetition_times[0])
                                asl_data["RepetitionTimePreparation"] = repetition_times[0]
                            elif len(repetition_times) < m0scan_count:
                                errors.append(
                                    f"Error: 'RepetitionTimePreparation' array in ASL file '{asl_filename}' is shorter"
                                    f" than the number of 'm0scan' in TSV file '{tsv_filename}'")
                    else:
                        if group['m0_json'] is None and asl_data.get("BackgroundSuppression") and asl_data.get(
                                "BackgroundSuppression"):
                            if asl_data.get("BackgroundSuppressionPulseTime"):
                                warnings.append(f"For {asl_filename}, no M0 is provided and BS pulses with known"
                                                f" timings are on. BS-pulse efficiency has to be calculated to"
                                                f" enable absolute quantification.")
                            else:
                                warnings.append(f"For {asl_filename}, no M0 is provided and BS pulses with unknown"
                                                f" timings are on, only a relative quantification is possible.")
                elif file_format == "nifti":
                    errors.append(f"Error: 'aslcontext.tsv' is missing for {asl_filename}")
                else:
                    # Analyze total acquired pairs for DICOM input
                    if 'lRepetitions' in asl_data:
                        total_acquired_pairs = math.ceil(int(asl_data['lRepetitions']) / 2)
                        asl_data['TotalAcquiredPairs'] = total_acquired_pairs
                    global_pattern = "control-label"

        data = {
            "data": asl_json_data,
            "filenames": asl_json_filenames,
        }

        (combined_major_errors, combined_major_errors_concise, combined_errors, combined_errors_concise,
         combined_warnings, combined_warnings_concise, combined_values) = ASLValidator().validate(data)

        ASLUtils.ensure_keys_and_append(combined_errors, "m0_error", errors)
        ASLUtils.ensure_keys_and_append(combined_warnings, "m0_warning", warnings)

        os.makedirs(os.path.dirname("/tmp/upload"), exist_ok=True)

        JSONWriter.write(combined_major_errors, config['paths']['major_error_report'])
        JSONWriter.write(combined_errors, config['paths']['error_report'])
        JSONWriter.write(combined_warnings, config['paths']['warning_report'])

        major_errors_concise_text = ASLUtils.extract_concise_error(combined_major_errors_concise)
        errors_concise_text = ASLUtils.extract_concise_error(combined_errors_concise)
        warnings_concise_text = ASLUtils.extract_concise_error(combined_warnings_concise)

        inconsistency_errors = ReportGenerator.extract_inconsistencies(combined_errors_concise)
        major_inconsistency_errors = ReportGenerator.extract_inconsistencies(combined_major_errors_concise)
        warning_inconsistency_errors = ReportGenerator.extract_inconsistencies(combined_warnings_concise)

        m0_concise_error, m0_concise_error_params = ASLUtils.condense_and_reformat_discrepancies(errors)
        m0_concise_warning, _ = ASLUtils.condense_and_reformat_discrepancies(warnings)

        M0_TR, report_line_on_M0 = ASLUtils.determine_m0_tr_and_report(m0_prep_times_collection, all_absent,
                                                                              bs_all_off, errors, m0_type=m0_type,
                                                                              inconsistent_params=m0_concise_error_params)

        asl_report, asl_parameters = ReportGenerator.generate_asl_report(combined_values, combined_major_errors,
                                                                         combined_errors, global_pattern, m0_type,
                                                                         total_acquired_pairs=total_acquired_pairs,
                                                                         slice_number=nifti_slice_number)
        m0_parameters = []
        m0_parameters.append(("M0 Type", m0_type))
        if M0_TR:
            m0_parameters.append(("M0 TR", M0_TR))
        m0_report = ReportGenerator.generate_m0_report(report_line_on_M0, M0_TR)
        basic_report = asl_report + m0_report
        ReportWriter.write(basic_report, config['paths']['basic_report'])

        extended_report, extended_parameters = ReportGenerator.generate_extended_report(combined_values,
                                                                                        combined_major_errors,
                                                                                        combined_errors)
        extended_report = asl_report + extended_report + m0_report
        ReportWriter.write(extended_report, config['paths']['extended_report'])

        asl_parameters = [(key, "True" if isinstance(value, bool) and value else value) for key, value in
                          asl_parameters]
        extended_parameters = [(key, "True" if isinstance(value, bool) and value else value) for
                               key, value in
                               extended_parameters]
        result = {
            "major_errors": combined_major_errors,
            "major_errors_concise": combined_major_errors_concise,
            "errors": combined_errors,
            "errors_concise": combined_errors_concise,
            "warnings": combined_warnings,
            "warnings_concise": combined_warnings_concise,
            "basic_report": basic_report,
            "extended_report": extended_report,
            "nifti_slice_number": nifti_slice_number,
            "major_errors_concise_text": major_errors_concise_text,
            "errors_concise_text": errors_concise_text,
            "warnings_concise_text": warnings_concise_text,
            "inconsistencies": "".join(inconsistency_errors),
            "major_inconsistencies": "".join(major_inconsistency_errors),
            "warning_inconsistencies": "".join(warning_inconsistency_errors),
            "m0_concise_error": "\n".join(m0_concise_error),
            "m0_concise_warning": "\n".join(m0_concise_warning),
            "asl_parameters": asl_parameters,
            "m0_parameters": m0_parameters,
            "extended_parameters": extended_parameters
        }

        return result
