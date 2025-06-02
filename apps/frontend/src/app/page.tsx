import { MetadataTable } from "@/components/MetadataTable";
import { MethodsPreview } from "@/components/MethodsPreview";
import { UploadPanel } from "@/components/UploadPanel";

export default function Home() {
  return (
    <div>
      <UploadPanel />
      <MetadataTable  metadata={{
        "Study ID": "123456",
        "Patient Name": "John Doe",
        "Date of Birth": "1990-01-01",
        "Scan Date": "2023-10-01",
        "Modality": "MRI",
        "Scanner Model": "Siemens Trio",
        "Field Strength": "3T",
        "Sequence Type": "T1-weighted",
        "Slice Thickness": "1mm",
        "Repetition Time (TR)": "2500ms",
        "Echo Time (TE)": "3.5ms",
      }} />
      <MethodsPreview content="str" />
    </div>
  );
}
