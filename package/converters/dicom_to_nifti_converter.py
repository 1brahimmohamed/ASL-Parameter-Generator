import os
import pydicom
import json
import subprocess
import re
import tempfile
from .base_converter import BaseConverter

class DICOM2NiftiConverter(BaseConverter):

    def __init__(self, dcm_files, upload_folder, nifti_file):
        self.dcm_files = dcm_files
        self.upload_folder = upload_folder
        self.nifti_file = nifti_file

    def convert(self):
        converted_files = []
        converted_filenames = []
        nifti_file_assigned = self.nifti_file
        processed_series = set()
        series_repetitions = {}

        with tempfile.TemporaryDirectory() as temp_dir:
            for dcm_file in self.dcm_files:
                dcm_filepath = os.path.join(temp_dir, dcm_file.filename)
                dcm_file.save(dcm_filepath)

                # Read DICOM file header
                ds = pydicom.dcmread(dcm_filepath)
                series_number_element = ds.get((0x0020, 0x0011), None)

                if series_number_element:
                    series_number = series_number_element.value
                    if series_number in processed_series:
                        continue  # Skip processing if this series has already been processed

                    processed_series.add(series_number)

                    # Print the line with "lRepetitions" if present
                    private_0029_1020 = ds.get((0x0029, 0x1020), None)
                    if private_0029_1020:
                        value = private_0029_1020.value.decode('latin1')  # Fallback to another encoding

                        match = re.search(r"lRepetitions\s*=\s*(\d+)", value)
                        if match:
                            lRepetitions_value = match.group(1)
                            series_repetitions[series_number] = lRepetitions_value

            # Check if there are any DICOM files in the temporary directory
            if not os.listdir(temp_dir):
                return None, None, self.nifti_file, "nifti", "No DICOM files found."

            # Ensure upload_folder exists
            os.makedirs(self.upload_folder, exist_ok=True)

            # Run dcm2niix on the temporary directory with the DICOM files
            try:
                result = subprocess.run(
                    ['dcm2niix', '-z', 'y', '-o', self.upload_folder, temp_dir],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print(result.stdout.decode())
            except subprocess.CalledProcessError as e:
                print(f"Error: {e.stderr.decode()}")
                return None, None, self.nifti_file, None, e.stderr.decode()

            # Collect the converted files
            for root, dirs, files in os.walk(self.upload_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file.endswith('.nii') or file.endswith('.nii.gz'):
                        if nifti_file_assigned is None:
                            nifti_file_assigned = file_path
                    elif file.endswith('.json'):
                        with open(file_path, 'r') as json_file:
                            json_data = json.load(json_file)

                        series_number = json_data.get('SeriesNumber', None)
                        if series_number and series_number in series_repetitions:
                            json_data['lRepetitions'] = series_repetitions[series_number]
                            with open(file_path, 'w') as json_file:
                                json.dump(json_data, json_file, indent=4)

                        converted_files.append(file_path)
                        converted_filenames.append(file)
                    else:
                        print(f"Error: Unexpected file format {file_path}")
                        return None, None, self.nifti_file, None, f"Unexpected file format: {file_path}"

        if nifti_file_assigned is None:
            return None, None, None, "nifti", "No NIfTI file was generated."

        return converted_files, converted_filenames, nifti_file_assigned, "dicom", None
