import MissingParameters from "@/components/reports/MissingParameters";
import BasicReport from "@/components/reports/BasicReport";
import ExtendedReport from "@/components/reports/ExtendedReport";
import CardWithTitle from "@/components/general/CardWithTitle";
import ParametersTable from "@/components/reports/ParametersTable";

export default function Home() {

    return (
        <div className="flex gap-4 h-full w-full p-5 ">

            <div className={"w-2/5"}>
                <CardWithTitle title={"Parameters"} className={"h-2/3"}>
                    <ParametersTable/>
                </CardWithTitle>

                <CardWithTitle title={"Missing Parameters"} className={"h-1/3"}>
                    <MissingParameters/>
                </CardWithTitle>

            </div>

            <div className={"flex flex-col gap-4 ml-4 h-full w-3/5"}>

                <CardWithTitle title={"Basic Report"} className={"h-2/5"}>
                    <BasicReport/>
                </CardWithTitle>


                <CardWithTitle title={"Extended Report"} className={"h-3/5"}>
                    <ExtendedReport/>
                </CardWithTitle>

            </div>
        </div>
    );
}
