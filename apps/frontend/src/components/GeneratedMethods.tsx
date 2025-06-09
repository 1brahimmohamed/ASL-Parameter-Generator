"use client";

import { useState, useRef } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "./ui/card";
import { Button } from "./ui/button";
import { ClipboardCopy } from "lucide-react";

export default function GeneratedMethods() {
    const [text, setText] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleCopy = () => {
        if (textareaRef.current) {
            navigator.clipboard.writeText(textareaRef.current.value)
                .then(() => {
                    // Optional: Add visual feedback for successful copy
                    console.log("Text copied to clipboard");
                })
                .catch(err => {
                    console.error("Failed to copy text: ", err);
                });
        }
    };

    return (
        <Card className="h-full py-0 p-2 bg-gray-50 dark:bg-secondary relative">
            <Button
                onClick={handleCopy}
                size="sm"
                variant="ghost"
                className="absolute top-2 right-2 z-10 hover:bg-gray-200 dark:hover:bg-gray-700"
                aria-label="Copy to clipboard"
            >
                <ClipboardCopy className="h-4 w-4" />
            </Button>
            <Textarea
                ref={textareaRef}
                className="w-full h-full border-none shadow-none bg-transparent dark:text-gray-200 dark:placeholder-gray-400"
                placeholder="Generated methods will appear here..."
                readOnly
                value={text}
                onChange={(e) => setText(e.target.value)}
            />
        </Card>
    );
}