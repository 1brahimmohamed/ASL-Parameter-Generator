import os
from fastapi import APIRouter, HTTPException, status, File, Form, UploadFile
from typing import List, Optional
from .data import data
from pyaslreport import generate_report
from pyaslreport.enums import ModalityTypeValues
from fastapi.responses import FileResponse
import tempfile
from weasyprint import HTML
from app.utils.report_template import render_report_html


report_router = APIRouter(prefix="/report")

# create the uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/dicom", exist_ok=True)

@report_router.post("/process", response_model=dict, status_code=status.HTTP_200_OK)
async def get_report(
        files: Optional[List[UploadFile]] = File(None),
        nifti_file: Optional[UploadFile] = File(None),
        dcm_files: Optional[List[UploadFile]] = File(None)
):
    """
    Receives form data and two files: a NIfTI file and a DICOM file.
    """
    data = {
        "modality": ModalityTypeValues.ASL,
        "files": [],
        "nifti_file": None,
        "dcm_files": []
    }

    # save the incoming files to the uploads directory
    if files:
        for file in files:
            file_path = await save_upload(file)
            data["files"].append(file_path)

    if nifti_file:
        file_path = await save_upload(nifti_file)
        data["nifti_file"] = file_path

    if dcm_files:
        for file in dcm_files:
            file_path = await save_upload(file, base_dir="uploads/dicom")
            data["dcm_files"].append(file_path)

    try: 
        report = generate_report(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return report


@report_router.post("/missing-parameters", response_model=dict, status_code=status.HTTP_200_OK)
async def submit_missing_parameters(missing_params: dict):
    """
    Receives a dictionary of missing parameters and their values.
    """
    print(missing_params)
    return {"message": "Missing parameters submitted successfully"}




@report_router.post("/report-pdf")
async def download_pdf(report_data: dict):
    print("--------------------------------")
    print(report_data["report_data"]["asl_parameters"])
    print("--------------------------------")
    html_content = render_report_html(report_data["report_data"])
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        HTML(string=html_content).write_pdf(tmp.name)
        tmp_path = tmp.name
    return FileResponse(tmp_path, media_type="application/pdf", filename="report.pdf")

async def save_upload(upload: UploadFile, base_dir="uploads"):
    # Use the filename as a relative path if needed
    file_path = os.path.join(base_dir, upload.filename)
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await upload.read())
    return file_path