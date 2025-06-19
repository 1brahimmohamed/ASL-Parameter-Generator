"use client";

import React, {createContext, useContext, useState, ReactNode} from 'react';
import {IReportApiResponse} from "@/types";

type AppContextType = {
    isLoading: boolean;
    setIsLoading: (isLoading: boolean) => void;
    apiData: IReportApiResponse;
    setApiData: (data: Partial<IReportApiResponse>) => void;
    clearApiData: () => void;
};

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider = ({children}: { children: ReactNode }) => {
    const [isLoading, setIsLoading] = useState(false);
    const [apiData, setApiDataState] = useState<IReportApiResponse>({});

    // Function to set new API data
    const setApiData = (data: Partial<ApiData>) => {
        setApiDataState(prevData => ({...data}));
    };

    // Function to clear API data
    const clearApiData = () => {
        setApiDataState({});
    };

    return (
        <AppContext.Provider value={{
            isLoading,
            setIsLoading,
            apiData,
            setApiData,
            clearApiData
        }}>
            {children}
        </AppContext.Provider>
    );
};

export const useAppContext = () => {
    const context = useContext(AppContext);
    if (context === undefined) {
        throw new Error('useAppContext must be used within a AppProvider');
    }
    return context;
};