"use client";
import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export const UploadPanel = () => {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold">Upload MRI Dataset</h3>
      <Label htmlFor="file-upload">Choose a file</Label>
      <Input id="file-upload" type="file" accept=".zip,.nii,.dcm" onChange={handleFileChange} />
      {file && <p className="text-sm text-muted-foreground">Selected: {file.name}</p>}
    </div>
  );
};