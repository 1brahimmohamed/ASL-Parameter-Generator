import GeneratedMethods from "@/components/GeneratedMethods";
import MissingParameters from "@/components/MissingParameters";
import Upload from "@/components/Upload";
import BasicReport from "@/components/BasicReport";
import ExtendedReport from "@/components/ExtendedReport";
import Errors from "@/components/Errors";

export default function Home() {

    return (
        <div className="flex flex-col gap-4 h-full w-full p-5 ">

            <div className={"flex flex-col h-3/5 gap-4"}>
                <h2 className={"text-2xl"}>
                    Upload
                </h2>
                <Upload/>
            </div>
        </div>
    );
}
