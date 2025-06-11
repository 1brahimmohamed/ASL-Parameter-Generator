from fastapi import APIRouter, HTTPException, status, File, Form, UploadFile
from typing import List, Optional

report_router = APIRouter()


@report_router.post("/report", response_model=dict, status_code=status.HTTP_200_OK)
async def get_report(
        files: Optional[List[UploadFile]] = File(None),
        nifti_file: Optional[UploadFile] = File(None),
        dcm_files: Optional[List[UploadFile]] = File(None)
):
    """
    Receives form data and two files: a NIfTI file and a DICOM file.
    """

    return {
        "message": "Files received",
        "files": [f.filename for f in files] if files else [],
        "nifti_file": nifti_file.filename if nifti_file else None,
        "dcm_files": [d.filename for d in dcm_files] if dcm_files else [],
    }