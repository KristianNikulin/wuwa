import React from "react";

import Header from "../../components/Header";

const NotAuth = () => {
    return (
        <div>
            <Header />
            <p>You don't have permissions for this page</p>
        </div>
    );
};

export default NotAuth;
