import Upload from "@/components/Upload";

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
