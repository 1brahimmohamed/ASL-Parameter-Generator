"use client";

import {useState ,useEffect} from "react";
import {useAppContext} from "@/providers/AppProvider";
import {Card} from "./ui/card";

const Errors = () => {

    const [errors, setErrors] = useState<string[]>([]);

    const {apiData} = useAppContext();

    useEffect(() => {
        if (apiData.m0_concise_error) {
            setErrors([apiData.m0_concise_error])
        } else {
            setErrors([]); // Clear errors when there's no error
        }
    }, [apiData]);

    return (
        <Card className="bg-red-50 h-full dark:bg-red-100 text-red-800 dark:text-red-200 p-4">
            <ul className="list-disc pl-5">
                {errors.map((error, index) => (
                    <li key={index} className="mb-1">{error}</li>
                ))}
            </ul>
        </Card>
    );
}

export default Errors;