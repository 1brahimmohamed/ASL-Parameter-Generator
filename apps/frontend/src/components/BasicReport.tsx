"use client";

import {useEffect, useState} from "react";
import {useAppContext} from "@/providers/AppProvider";
import GeneratedMethods from "@/components/GeneratedMethods";

const BasicReport = () => {
    const [text, setText] = useState("");
    const {apiData} = useAppContext();


    useEffect(() => {
        if (apiData && apiData.basic_report) {
            setText(apiData.basic_report);
        }
    }, [apiData]);


    return (
        <GeneratedMethods text={text} />
    )

}

export default BasicReport;