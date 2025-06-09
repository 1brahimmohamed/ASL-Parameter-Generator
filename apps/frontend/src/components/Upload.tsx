"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import ParametersTable from "@/components/ParametersTable";
import { Button } from "@/components/ui/button";
import { Upload as UploadIcon } from "lucide-react";

export default function Upload() {
    const [activeOption, setActiveOption] = useState<"option1" | "option2">("option1");

    return (
        <Card className="flex flex-col p-4 gap-4 bg-gray-50 dark:bg-secondary">
            <div className={"flex items-center justify-between mb-4"}>
                <div className="flex w-fit">
                    <Button
                        type="button"
                        className={`rounded-l-md rounded-r-none border border-input ${
                            activeOption === "option1"
                                ? "bg-primary text-primary-foreground"
                                : "bg-background text-foreground hover:bg-accent hover:text-accent-foreground"
                        }`}
                        onClick={() => setActiveOption("option1")}
                    >
                        BDIS
                    </Button>
                    <Button
                        type="button"
                        className={`rounded-r-md rounded-l-none border-t border-b border-r border-input -ml-px ${
                            activeOption === "option2"
                                ? "bg-primary text-primary-foreground"
                                : "bg-background text-foreground hover:bg-accent hover:text-accent-foreground"
                        }`}
                        onClick={() => setActiveOption("option2")}
                    >
                        DICOM
                    </Button>
                </div>

                <div>
                    <Button className={"hover:pointer"}>
                        <UploadIcon />
                        {activeOption === "option1" ? "Upload BDIS" : "Upload DICOM"}
                    </Button>
                </div>
            </div>

            <div>
                <ParametersTable />
            </div>
        </Card>
    );
}