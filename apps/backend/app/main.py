from fastapi import FastAPI
from .routers import report_router

app = FastAPI()
app.include_router(report_router)

@app.get("/")
def read_root():
    return {
        "name": "ASL Methods Parameter Generator API Service",
        "version": "0.0.1",
        "description": "This service provides an API for generating ASL methods parameters based on user input. "
                       "It is designed to be used in conjunction with the ASL Methods Parameter Generator frontend application.",
        "organization": "The ISMRM Open Science Initiative for Perfusion Imaging",
        "authors": [
            "Ibrahim Abdelazim",
            "Hanliang Xu"
        ],
        "supervisors": [
            "Jan Petr",
            "David Thomas",
        ],
        "license": "MIT",
    }
