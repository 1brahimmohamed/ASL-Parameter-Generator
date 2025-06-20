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

            <div className={"flex gap-4 h-2/5"}>

                <div className={"flex flex-col w-1/3 gap-4"}>
                    <h2 className={"text-2xl"}>
                        Missing Parameters
                    </h2>
                    <MissingParameters/>
                </div>

                <div className={"flex flex-col w-2/3 gap-4"}>
                    <h2 className={"text-2xl"}>
                        Basic Report
                    </h2>
                    <BasicReport/>
                </div>

            </div>
            <div className={"flex gap-4 h-2/5"}>

                <div className={"flex flex-col w-1/3 gap-4"}>
                    <h2 className={"text-2xl"}>
                        Errors
                    </h2>
                    <Errors/>
                </div>

                <div className={"flex flex-col w-2/3 gap-4"}>
                    <h2 className={"text-2xl"}>
                        Extended Report
                    </h2>
                    <ExtendedReport/>
                </div>

            </div>
        </div>
    );
}
