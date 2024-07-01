import React, { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from "../provider/AuthProvider";
import { useCookies } from 'react-cookie';

import { Avatar } from 'primereact/avatar';
import { TieredMenu } from 'primereact/tieredmenu';
import '../styles/UserDropdown.css';
import Placeholder from "../assets/user-placeholder.png"

const UserDropdown = () => {
    const menu = useRef(null);
    const navigate = useNavigate();
    const { setToken } = useAuth();
    const [cookies, setCookie] = useCookies(['ml-auth-jwt']);

    const items = [
        {
            label: 'Logout',
            icon: 'pi pi-sign-out',
            command: () => {
                setToken();
                setCookie('ml-auth-jwt', null);
                navigate("/")
            }
        }
    ];

    return (
        <div className="user-dropdown">
            <TieredMenu model={items} popup ref={menu} breakpoint="767px" />
            <Avatar image={Placeholder} shape="circle" className='avatar' onClick={(e) => menu.current.toggle(e)} />
        </div>
    )
}

export default UserDropdown;
