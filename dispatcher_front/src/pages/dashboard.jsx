import PropTypes from "prop-types";

import auth_service from "../api/auth.jsx";
import {Outlet, useNavigate} from "react-router-dom";
import {useState} from "react";


const MobileHeaderView = ({set_show}) => {
    const navigate = useNavigate();

    const handleOuterClick = () => {
        set_show(false);
    };

    const nav = (path) => {
        set_show(false);
        navigate(path);
    }

    const handleInnerClick = (e) => {
        e.stopPropagation(); // Останавливаем всплытие события
    };

    return <div className='overlay-backdrop' onClick={() => handleOuterClick()}>
        <div className='overlay-content base_flex_column rounded_border' style={{
            flexWrap: 'nowrap',

            backgroundColor: 'var(--header-color)',
            color: 'var(--header-text-color)',

            height: '30vh',
            width: '80%',
        }} onClick={(e) => handleInnerClick(e)}>
            <a className='header_a_c' style={
                window.location.pathname === '/' ? {
                    backgroundColor: 'var(--header-current-color)',
                    color: 'var(--header-current-text-color)',
                }: null
            } onClick={() => nav('/')}>Инциденты</a>
            <a className='header_a_c' style={
                window.location.pathname === '/apps' ? {
                    backgroundColor: 'var(--header-current-color)',
                    color: 'var(--header-current-text-color)',
                }: null
            } onClick={() => nav('/apps')}>Приложения</a>
            <a className='header_a_c' style={{
                marginRight: '5px',
            }} onClick={() => auth_service.logout()}>Выйти</a>
        </div>
    </div>
}
MobileHeaderView.propTypes = {
    set_show: PropTypes.func.isRequired,
}


const DashboardHeader = () => {
    const navigate = useNavigate();

    const [mobile_show_view, set_mobile_show_view] = useState(false);

    function get_current_window() {
        if (window.location.pathname === '/') {
            return 'Инциденты'
        }
        if (window.location.pathname === '/apps') {
            return 'Приложения'
        }
    }

    return <header style={{
        backgroundColor: 'var(--header-color)',
        width: '100%',
        height: '50px',
    }}>
        <div className='desktop base_flex_row' style={{
            backgroundColor: 'var(--header-color)',
            alignItems: 'center',
            height: '100%',
        }}>
            <span style={{
                userSelect: 'none',
                fontWeight: 'bolder',
                fontStyle: 'italic',
                color: 'var(--header-text-color)',
                padding: '3px',
                fontSize: '20px',
                margin: '0 5px',
            }}>NCT DISPATCHER</span>
            <a className='header_a' style={
                window.location.pathname === '/' ? {
                    backgroundColor: 'var(--header-current-color)',
                    color: 'var(--header-current-text-color)',
                }: null
            } onClick={() => navigate('/')}>Инциденты</a>
            <a className='header_a' style={
                window.location.pathname === '/apps' ? {
                    backgroundColor: 'var(--header-current-color)',
                    color: 'var(--header-current-text-color)',
                }: null
            } onClick={() => navigate('/apps')}>Приложения</a>
            <a className='header_a' style={{
                marginLeft: 'auto',
            }}>{auth_service.user()}</a>
            <a className='header_a' style={{
                marginRight: '5px',
            }} onClick={() => auth_service.logout()}>Выйти</a>
        </div>
        <div className='mobile base_flex_row' style={{
            backgroundColor: 'var(--header-color)',
            alignItems: 'center',
            height: '100%',
        }}>
            <span style={{
                userSelect: 'none',
                fontWeight: 'bolder',
                color: 'var(--header-text-color)',
                padding: '3px',
                margin: '0 5px',
            }}>{auth_service.user()} > {get_current_window()}</span>
            <button className='header_a' style={{
                marginLeft: 'auto',
                marginRight: '5px',
                padding: '15px',
                color: 'var(--header-current-text-color)',
                backgroundColor: 'var(--header-color)',
            }} onClick={() => set_mobile_show_view(!mobile_show_view)}>···</button>
            {mobile_show_view && <MobileHeaderView set_show={set_mobile_show_view}/>}
        </div>
    </header>
}


const Dashboard = () => {
    return <div>
        <DashboardHeader />
        <Outlet />
    </div>
}

export default Dashboard;