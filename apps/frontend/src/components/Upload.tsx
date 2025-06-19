"use client";

import React, {useState, useRef} from "react";
import {Upload as UploadIcon} from "lucide-react";
import ParametersTable from "@/components/ParametersTable";
import {Card} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {findNiftiFile, findRelevantFiles} from "@/utils";
import {getReport} from "@/services/apiReport";
import UploadTypes from "@/enums/UploadTypes";
import {cn} from "@/lib/utils";
import {useAppContext} from "@/providers/AppProvider";
import {toast} from "react-hot-toast";

type TUploadOptions = typeof UploadTypes[keyof typeof UploadTypes];

export default function Upload() {
    const [activeOption, setActiveOption] = useState<TUploadOptions>(UploadTypes.BDIS);
    const folderInputRef = useRef<HTMLInputElement>(null);

    const {setIsLoading, setApiData} = useAppContext();

    const handleDirectoryUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const files: FileList | null = e.target.files;

        if (files && files.length > 0) {

            // Show the spinner
            setIsLoading(true);

            const filesArray = Array.from(files);
            const niftiFile = findNiftiFile(filesArray);
            const aslRelevantFiles = findRelevantFiles(filesArray);

            const formData = new FormData();

            // nifti file
            if (niftiFile) {
                formData.append('nifti_file', niftiFile);
            }

            // diocm files
            filesArray.forEach(file => {
                if (file.name.endsWith('.dcm')) {
                    formData.append('dcm_files', file);
                }
            });

            // asl relevant files
            aslRelevantFiles.forEach(file => {
                formData.append('files', file);
                formData.append('filenames', file.name);
            });

            const data = await getReport(formData);

            // Hide the spinner
            setIsLoading(false);

            if (data) {
                setApiData(data);
                toast.success("Report generated successfully!");

            } else {
                toast.error("Failed to generate report. Please check the files and try again.");
            }
        }
    };

    const handleUploadClick = () => {
        folderInputRef.current?.click();
    };

    return (
        <Card className="flex flex-col p-4 gap-4 bg-gray-50 dark:bg-secondary">
            <div className={"flex items-center justify-between mb-4"}>
                <div className="flex w-fit">
                    <Button
                        type="button"
                        className={cn(
                            "rounded-l-md rounded-r-none border border-input cursor-pointer",
                            activeOption === UploadTypes.BDIS
                                ? "bg-primary text-primary-foreground"
                                : "bg-background text-foreground hover:bg-accent hover:text-accent-foreground"
                        )}
                        onClick={() => setActiveOption(UploadTypes.BDIS)}
                    >
                        BDIS
                    </Button>
                    <Button
                        type="button"
                        className={cn(
                            "rounded-r-md rounded-l-none border-t border-b border-r border-input -ml-px cursor-pointer",
                            activeOption === UploadTypes.DICOM
                                ? "bg-primary text-primary-foreground"
                                : "bg-background text-foreground hover:bg-accent hover:text-accent-foreground"
                        )}
                        onClick={() => setActiveOption(UploadTypes.DICOM)}
                    >
                        DICOM
                    </Button>
                </div>

                <div>
                    <input
                        type="file"
                        ref={folderInputRef}
                        onChange={handleDirectoryUpload}
                        style={{display: 'none'}}
                        {...{webkitdirectory: "", directory: ""}}
                    />

                    <Button className={"cursor-pointer"} onClick={handleUploadClick}>
                        <UploadIcon/>
                        Upload {activeOption === UploadTypes.BDIS ? "BDIS" : "DICOM"}
                    </Button>
                </div>
            </div>

            <div>
                <ParametersTable/>
            </div>
        </Card>
    );
}