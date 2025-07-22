'use client'
import {Card} from "@/components/ui/card";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";
import {useAppContext} from "@/providers/AppProvider";
import React, {useState} from "react";
import { Check, AlertCircle } from "lucide-react";
import { postMissingParameters } from "@/services/apiReport";

export default function MissingParameters() {
    const {apiData} = useAppContext();
    const missingParams = apiData?.missing_required_parameters || [];
    const [paramValues, setParamValues] = useState<Record<string, string>>({});

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const filledParams = Object.fromEntries(
            Object.entries(paramValues).filter(([k, v]) => v && missingParams.includes(k))
        );
        postMissingParameters(filledParams)
    };

    if (!missingParams.length) {
        return (
            <Card className="h-full p-2 bg-gray-50 dark:bg-secondary flex items-center justify-center text-muted-foreground">
                No missing parameters!
            </Card>
        );
    }

    return (
        <Card className="h-full p-2 bg-gray-50 dark:bg-secondary flex flex-col justify-between">
            <div>
                <h3 className="font-semibold mb-2 text-base">Missing Parameters</h3>
                <ul className="flex flex-col gap-1 max-h-48 overflow-y-auto pr-1 mb-2">
                    {missingParams.map(param => {
                        const filled = paramValues[param] && paramValues[param].trim();
                        return (
                            <li key={param} className="flex justify-between items-center gap-2 p-1 rounded bg-white dark:bg-muted/30 border border-muted/30">
                                <div className="flex items-center gap-2">
                                    {filled ? (
                                        <Check className="text-green-600 w-4 h-4" />
                                    ) : (
                                        <AlertCircle className="text-red-500 w-4 h-4" />
                                    )}
                                    <span className="font-medium w-48 truncate">{param}</span>
                                </div>
                                <Input
                                    className="border-none px-1 py-0 h-7 text-sm focus:ring-0 focus-visible:ring-0 focus:border-none focus:outline-none shadow-none max-w-52 text-left"
                                    style={{minWidth: 0}}
                                    placeholder="Value"
                                    value={paramValues[param] || ""}
                                    onChange={e =>
                                        setParamValues(prev => ({
                                            ...prev,
                                            [param]: e.target.value
                                        }))
                                    }
                                />
                            </li>
                        );
                    })}
                </ul>
            </div>
            <form className="flex flex-col gap-2 mt-2" onSubmit={handleSubmit}>
                <Button
                    type="submit"
                    disabled={missingParams.some(param => !(paramValues[param] && paramValues[param].trim()))}
                    className="w-full mt-auto"
                >
                    Submit Missing Parameters
                </Button>
            </form>
        </Card>
    );
}

