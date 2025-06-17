import axios from 'axios';
import {IReportApiResponse} from '@/types';


const API_BASE_URL = `${process.env.NEXT_PUBLIC_API_BASE_URL}/report`;

const client = axios.create({
    baseURL: API_BASE_URL,
});

/**
 * Fetches a report based on the provided form data.
 * @param formData - The FormData object containing the files to be processed.
 * @return IReportApiResponse - A promise that resolves to the report data.
 */
const getReport = async (formData: FormData): Promise<any> => {
    try {
        const response = await client.post(
            '/process',
            formData
        );

        return response.data;
    } catch (error) {
        console.error('Error fetching report:', error);
        throw error;
    }
}

export {
    getReport,
}