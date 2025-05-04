import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { AdminFormProvider } from "./../../state-providers/AdminContext/index";
import { useUser } from "../../state-providers/UserContext";

import { GalogramsStep } from "./GalogramsStep";

import styles from "./styles.module.scss";

export const Admin = () => {
    const navigate = useNavigate();
    const { user } = useUser();

    useEffect(() => {
        const isAdmin = user?.status === "admin";
        user?.status && !isAdmin && navigate("/401");
    }, [user, navigate]);

    return (
        <AdminFormProvider>
            {({ step }) => (
                <div className={styles.adminContainer}>
                    {step === 1 && <GalogramsStep />}
                    {/* {step === 2 && <GalogramsStep />} */}
                    {/* {step === 2 && <AdditionalInfoStep />} */}
                    {/* {step === 3 && <ConfirmationStep />} */}
                </div>
            )}
        </AdminFormProvider>
    );
};

export default Admin;
