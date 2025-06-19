import nibabel as nib


class NiftiReader:
    """
    A class to read NIfTI files.
    This is a placeholder for the actual implementation.
    """

    @staticmethod
    def read(nifti_file):
        try:
            if isinstance(nifti_file, str):
                if not nifti_file.endswith(('.nii', '.nii.gz')):
                    return None, f"Invalid file: {nifti_file}"

                nifti_filepath = nifti_file

            else:
                raise ValueError("Unsupported file type. Expected a string path to a NIfTI file.")

            nifti_img = nib.load(nifti_filepath)
            slice_count = nifti_img.shape[2]
            return slice_count

        except Exception as e:
            raise RuntimeError(f"Error reading NIfTI file: {str(e)}") from e
