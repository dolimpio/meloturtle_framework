import React from 'react';
import { useNavigate } from "react-router-dom";
import { useAuth } from "../provider/AuthProvider";
import { Menubar } from 'primereact/menubar';
import { Button } from 'primereact/button';
import UserDropdown from "./UserDropdown";
import Logo from "../assets/logo-meloturtle.png"


const Navbar = () => {
    const navigate = useNavigate();
    const { token } = useAuth();

    const items = [
        {
            label: 'Home',
            icon: 'pi pi-home',
            command: () => {
                navigate('/');
            }
        },
        {
            label: 'About',
            icon: 'pi pi-info-circle',
            command: () => {
                navigate('/about');
            }
        }
    ];

    const loggedItems = [
        {
            label: 'Home',
            icon: 'pi pi-home',
            command: () => {
                navigate('/');
            }
        },
        {
            label: 'Generator',
            icon: 'pi pi-bolt',
            command: () => {
                navigate('/generator');
            }
        },
        {
            label: 'My playlists',
            icon: 'pi pi-play',
            command: () => {
                navigate('/library');
            }
        },
        {
            label: 'About',
            icon: 'pi pi-info-circle',
            command: () => {
                navigate('/about');
            }
        }
    ];    
    const loggedEnd = (
        <div className="flex align-items-center gap-2">
            <UserDropdown />
        </div>
    );

    const end = (
        <div className="flex align-items-center gap-2">
            <Button label="Sign in" onClick={() => {
                navigate('/login');
            }} />
        </div>

    );

    const start = <img alt="logo" src={Logo} height="60" className="mr-2"></img>;
    

    return (
        <>
        <Menubar model={token ? loggedItems : items} start={start} end={token ? loggedEnd : end} />
        </>
    )
};

export default Navbar;