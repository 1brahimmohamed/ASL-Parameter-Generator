"use client";

import {useEffect, useState} from "react";
import {useAppContext} from "@/providers/AppProvider";
import WarningsCard from "@/components/warnings/WarningsCard";


const Page = () => {

    const [warnings, setWarnings] = useState<string[]>([]);

    const {apiData} = useAppContext();

    useEffect(() => {
        if (apiData.m0_concise_warning) {
            setWarnings([apiData.m0_concise_warning])
        } else {
            setWarnings([]); // Clear warnings when there's no error
        }
    }, [apiData]);

    if (warnings.length === 0) {
        return <NoWarnings/>;
    }


    return (
        <div className="flex flex-col gap-4 h-full w-full p-5">
            <div className={"grid grid-cols-2 gap-4 h-full w-full"}>
                <WarningsCard warnings={warnings} title="M0 Concise Errors"/>
                <WarningsCard warnings={warnings} title="Errors Concise"/>
                <WarningsCard warnings={warnings} title="Major Errors"/>
                <WarningsCard warnings={warnings} title="Major Errors Concise"/>
            </div>
        </div>
    );
}


const NoWarnings = () => {
    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">Warnings</h1>
            <p className="text-gray-600">No warnings to display.</p>
        </div>
    );
}

export default Page;