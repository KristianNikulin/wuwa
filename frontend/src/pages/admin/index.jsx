import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AdminProvider, useAdmin } from "./../../state-providers/AdminContext/index";
import { useUser } from "../../state-providers/UserContext";
import { GalogramsStep } from "./GalogramsStep";
import styles from "./styles.module.scss";
import { PickBansStep } from "./PickBansStep";

const AdminContent = () => {
    const { step } = useAdmin();
    const navigate = useNavigate();
    const { user } = useUser();

    useEffect(() => {
        const isAdmin = user?.status === "admin";
        user?.status && !isAdmin && navigate("/401");
    }, [user, navigate]);

    return (
        <div className={styles.adminContainer}>
            {step === 1 && <GalogramsStep />}
            {step === 2 && <PickBansStep />}
        </div>
    );
};

export const Admin = () => {
    return (
        <AdminProvider>
            <AdminContent />
        </AdminProvider>
    );
};

export default Admin;
