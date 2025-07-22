import {IReportApiResponse} from "@/types";

const countErrorsAndWarnings = (apiData: IReportApiResponse) => {
    if (!apiData || Object.keys(apiData).length === 0) {
        return { errorCount: 0, warningCount: 0 };
    }

    let errorCount = 0;
    let warningCount = 0;

    // Count M0 errors
    if (apiData.errors?.m0_error) {
        errorCount += apiData.errors.m0_error.length;
    }

    // Count major errors
    if (apiData.major_errors && typeof apiData.major_errors === 'object') {
        errorCount += Object.keys(apiData.major_errors).length;
    }

    // Count regular errors
    if (apiData.errors_concise && typeof apiData.errors_concise === 'object') {
        errorCount += Object.keys(apiData.errors_concise).length;
    }

    // Count warnings
    if (apiData.warnings && typeof apiData.warnings === 'object') {
        warningCount += Object.keys(apiData.warnings).length;
    }

    // Count concise warnings
    if (apiData.warnings_concise && typeof apiData.warnings_concise === 'object') {
        warningCount += Object.keys(apiData.warnings_concise).length;
    }

    return { errorCount, warningCount };
};

export { countErrorsAndWarnings };