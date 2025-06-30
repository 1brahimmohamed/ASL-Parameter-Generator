type Parameter = [string, string | number];

interface IReportApiResponse {
    asl_parameters: Parameter[];
    basic_report: string;
    errors: {
        m0_error: string[][];
    };
    errors_concise: Record<string, unknown>;
    errors_concise_text: string;
    extended_parameters: Parameter[];
    extended_report: string;
    inconsistencies: string;
    m0_concise_error: string;
    m0_concise_warning: string;
    m0_parameters: Parameter[];
    major_errors: Record<string, unknown>;
    major_errors_concise: Record<string, unknown>;
    major_errors_concise_text: string;
    major_inconsistencies: string;
    nifti_slice_number: number;
    warning_inconsistencies: string;
    warnings: Record<string, unknown>;
    warnings_concise: Record<string, unknown>;
    warnings_concise_text: string;
}

export default IReportApiResponse;
