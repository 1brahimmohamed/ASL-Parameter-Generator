"use client";

import ErrorsCard from "@/components/errors/ErrorsCard";
import {useEffect, useState} from "react";
import {useAppContext} from "@/providers/AppProvider";
import CardWithTitle from "@/components/general/CardWithTitle";

const Page = () => {

    const [errors, setErrors] = useState<string[]>([]);

    const {apiData} = useAppContext();

    useEffect(() => {
        if (apiData.m0_concise_error) {
            setErrors([apiData.m0_concise_error])
        } else {
            setErrors([]); // Clear errors when there's no error
        }
    }, [apiData]);

    if (errors.length === 0) {
        return <NoErrors/>;
    }


    return (
        <div className="flex flex-col gap-4 h-full w-full p-5">
            <div className={"grid grid-cols-2 gap-4 h-full w-full"}>
               
                <ErrorsCard errors={errors} title="M0 Concise Errors"/>
                    
                <ErrorsCard errors={errors} title="Errors Concise"/>

                <ErrorsCard errors={errors} title="Major Errors"/>

                <ErrorsCard errors={errors} title="Major Errors Concise"/>

            </div>
        </div>
    );
}

const NoErrors = () => {
    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">Errors</h1>
            <p className="text-gray-600">No errors found.</p>
        </div>
    );
}

export default Page;