import { Outlet } from "react-router-dom";
import React from 'react';
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import 'primeflex/primeflex.css'; // Import PrimeFlex CSS

const Layout = () => {
    return (
        <>
            <div className="p-d-flex p-flex-column layout-main-container" style={{ minHeight: '100vh' }}>
                <div className="p-flex-none layout-main-navbar">
                    <Navbar />
                </div>
                <div className="p-flex-grow-1 p-d-flex p-flex-column layout-main">
                    <Outlet />
                </div>
                <div className="p-flex-none layout-main-footer"  >
                    <Footer />
                </div>
            </div>
        </>
    )
};

export default Layout;
