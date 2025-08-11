"use client";

import React, { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { UploadDataType, UploadModalityType } from "@/enums";
import { Upload as UploadIcon } from "lucide-react";
import { useAppContext } from "@/providers/AppProvider";
import { findNiftiFile, findRelevantFiles } from "@/utils";
import { getReport } from "@/services/apiReport";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { IAllRelevantFilesType } from "@/types";

type TUploadDataOptions = (typeof UploadDataType)[keyof typeof UploadDataType];
type TUploadModalOptions =
  (typeof UploadModalityType)[keyof typeof UploadModalityType];


const UploadButtons = () => {
  const [activeFileTypeOption, setActiveFileTypeOption] =
    useState<TUploadDataOptions>(UploadDataType.BDIS);
  const [activeModalityTypeOption, setActiveModalityTypeOption] =
    useState<TUploadModalOptions>(UploadModalityType.ASL);
  const folderInputRef = useRef<HTMLInputElement>(null);
  const { setIsLoading, setApiData, setUploadedFiles, setUploadConfig } =
    useAppContext();
  const router = useRouter();

  const handleDirectoryUpload = async (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const files: FileList | null = e.target.files;

    if (files && files.length > 0) {
      setIsLoading(true);
      try {
        const filesArray = Array.from(files);

        const niftiFile = findNiftiFile(filesArray);
        const aslRelevantFiles = findRelevantFiles(filesArray);

        const allRelevantFiles: IAllRelevantFilesType = {
          nifti_file: niftiFile,
          asl_files: aslRelevantFiles,
          dicom_files: [],
        };

        const formData = new FormData();
        if (niftiFile) {
          formData.append("nifti_file", niftiFile);
        }
        filesArray.forEach((file) => {
          if (file.name.endsWith(".dcm")) {
            formData.append("dcm_files", file);
            allRelevantFiles.dicom_files.push(file);
          }
        });
        aslRelevantFiles.forEach((file) => {
          formData.append("files", file);
          formData.append("filenames", file.name);
        });


        // Store files and config for potential re-upload
        setUploadedFiles(allRelevantFiles);
        
        setUploadConfig({
          modalityType: activeModalityTypeOption,
          fileType: activeFileTypeOption,
        });

        formData.append("modality_type", activeModalityTypeOption);
        formData.append("files_type", activeFileTypeOption);

        console.log("Uploaded formdata structure:", formData);
        const data = await getReport(formData);
        setIsLoading(false);
        if (data) {
          setApiData(data);
          if (
            data.missing_required_parameters &&
            data.missing_required_parameters.length > 0
          ) {
            toast.info(
              "Report generated with missing parameters. Please provide the missing values."
            );
          } else {
            toast.success("Report generated successfully!");
          }
          router.push("/report");
        } else {
          toast.error(
            "Failed to generate report. Please check the files and try again."
          );
        }
      } catch (error) {
        setIsLoading(false);
        toast.error(
          `An unexpected error occurred during upload, please try again. Error: ${error}`
        );
      }
    }
  };

  const handleUploadClick = () => {
    folderInputRef.current?.click();
  };

  return (
    <div className={"flex items-center justify-between mb-4"}>
      <div className={"flex gap-4"}>
        {/* Modality Select */}
        <fieldset className="flex w-fit" aria-label="Select Modality Type">
          <legend className="sr-only">Modality Type</legend>
          <Button
            type="button"
            className={cn(
              "rounded-l-md rounded-r-none border border-input cursor-pointer",
              activeModalityTypeOption === UploadModalityType.ASL
                ? "bg-primary text-primary-foreground"
                : "bg-background text-foreground hover:bg-accent hover:text-accent-foreground"
            )}
            onClick={() => setActiveModalityTypeOption(UploadModalityType.ASL)}
          >
            ASL
          </Button>
          <Button
            type="button"
            className={cn(
              "rounded-r-md rounded-l-none border-t border-b border-r border-input -ml-px cursor-pointer",
              activeModalityTypeOption === UploadModalityType.DCE
                ? "bg-primary text-primary-foreground"
                : "bg-background text-foreground hover:bg-accent hover:text-accent-foreground"
            )}
            onClick={() => setActiveModalityTypeOption(UploadModalityType.DCE)}
          >
            DCE
          </Button>
        </fieldset>
        {/* Files Type Select */}
        <fieldset className="flex w-fit" aria-label="Select File Type">
          <legend className="sr-only">File Type</legend>
          <Button
            type="button"
            className={cn(
              "rounded-l-md rounded-r-none border border-input cursor-pointer",
              activeFileTypeOption === UploadDataType.BDIS
                ? "bg-primary text-primary-foreground"
                : "bg-background text-foreground hover:bg-accent hover:text-accent-foreground"
            )}
            onClick={() => setActiveFileTypeOption(UploadDataType.BDIS)}
          >
            BDIS
          </Button>
          <Button
            type="button"
            className={cn(
              "rounded-r-md rounded-l-none border-t border-b border-r border-input -ml-px cursor-pointer",
              activeFileTypeOption === UploadDataType.DICOM
                ? "bg-primary text-primary-foreground"
                : "bg-background text-foreground hover:bg-accent hover:text-accent-foreground"
            )}
            onClick={() => setActiveFileTypeOption(UploadDataType.DICOM)}
          >
            DICOM
          </Button>
        </fieldset>
      </div>
      <div>
        <input
          type="file"
          ref={folderInputRef}
          onChange={handleDirectoryUpload}
          style={{ display: "none" }}
          {...{ webkitdirectory: "", directory: "" }}
        />
        <Button
          className={"cursor-pointer"}
          onClick={handleUploadClick}
          aria-label={`Upload ${activeModalityTypeOption} ${activeFileTypeOption} files`}
        >
          <UploadIcon />
          Upload {activeModalityTypeOption} {activeFileTypeOption}
        </Button>
      </div>
    </div>
  );
};

export default UploadButtons;
