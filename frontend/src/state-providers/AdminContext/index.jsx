import React, { createContext, useContext, useState } from "react";
import { useForm } from "react-hook-form";

const AdminFormContext = createContext();

export const AdminFormProvider = ({ children }) => {
    const [step, setStep] = useState(1);
    const formMethods = useForm();

    const nextStep = () => setStep((prev) => prev + 1);
    const prevStep = () => setStep((prev) => prev - 1);

    return (
        <AdminFormContext.Provider value={{ step, nextStep, prevStep, ...formMethods }}>
            {typeof children === "function" ? children({ step, nextStep, prevStep, ...formMethods }) : children}
        </AdminFormContext.Provider>
    );
};

export const useAdminForm = () => useContext(AdminFormContext);
