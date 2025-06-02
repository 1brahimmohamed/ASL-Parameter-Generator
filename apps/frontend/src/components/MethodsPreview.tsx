"use client"
import React from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export const MethodsPreview = ({ content }: { content: string }) => {
  return (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold">Generated Methods Section</h3>
      <Textarea className="h-64" value={content} readOnly />
      <Button onClick={() => navigator.clipboard.writeText(content)}>
        Copy to Clipboard
      </Button>
    </div>
  );
};