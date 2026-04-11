import {Link, useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import {useAuth} from "@/context/auth.jsx";
import {useTheme} from "@/context/theme.jsx";
import dark from '/dark.svg'
import light from '/light.svg'
import useDevice from "@/context/mobile.jsx";


function is_current_window(path) {
    return window.location.pathname.startsWith(path)
}
function get_current_window(headers) {
    for (const i of headers) {
        if (window.location.pathname.startsWith(i.path)) {
            return i.label
        }
    }
    return ''
}


const MobileHeaderView = ({headers, set_show}) => {
    const navigate = useNavigate();
    const mobile_headers = parse_mobile_headers(headers);

    function parse_mobile_headers() {
        const new_headers = [];
        for (const i of headers) {
            if (!is_current_window(i.path)) {
                new_headers.push(i);
            }
        }
        return new_headers;
    }

    const handleOuterClick = () => {
        set_show(false);
    };

    const handleInnerClick = (e) => {
        e.stopPropagation(); // Останавливаем всплытие события
    };

    const nav = (path) => {
        set_show(false);
        navigate(path);
    }

    return <div className='header_overlay-backdrop' onClick={() => handleOuterClick()}>
        <div className='header_overlay-content base_flex_column rounded_border' style={{
            flexWrap: 'nowrap',

            backgroundColor: 'var(--header-color)',
            color: 'var(--header-text-color)',

            height: '30vh',
            padding: '5px'
        }} onClick={(e) => handleInnerClick(e)}>
            {mobile_headers.map((header, i) => <div key={i} style={{
                backgroundColor: is_current_window(header.path) ? 'var(--header-current-color)': 'inherit',
                color: is_current_window(header.path) ? 'var(--header-current-text-color)': 'var(--header-text-color)',
                textDecoration: 'none',
                ...header.m_style,
            }} onClick={() => nav(header.path)} className='header_a_c'>{header.label}</div>)}
        </div>
    </div>
}


const CustomHeader = ({logo, headers}) => {
    const { user } = useAuth();
    const { theme, set_theme } = useTheme();
    const { isMobile } = useDevice();

    const [mobile_show_view, set_mobile_show_view] = useState(false);

    const handle_theme = (new_theme) => {
        set_theme(new_theme);
    }

    const adt_headers = [
        {
            path: undefined,
            label: theme === 'dark' ? <img src={light} alt="светлая тема" style={{
                width: '25px',
                height: '25px',
                backgroundColor: 'var(--header-color)',
                padding: '1px',
            }} onClick={() => handle_theme('light')}/>: <img src={dark} alt="темная тема" style={{
                width: '25px',
                height: '25px',
                backgroundColor: 'var(--header-color)',
                padding: '1px',
            }} onClick={() => handle_theme('dark')}/>,
            d_style: {
                marginLeft: 'auto',
                marginRight: '10px',
            }
        },
        ...user.name === null || user.name === undefined ? [{
            path: '/auth/login',
            label: 'Вход',
            d_style: {
                marginRight: '10px',
            }
        }]:[{
            path: '/auth/logout',
            label: `Выход (${user.name})`,
            d_style: {
                marginRight: '10px',
            }
        }],
    ]
    const full_headers = [...headers, ...adt_headers]

    useEffect(() => {

    }, []);

    return <header>
        {logo}
        {isMobile ? (
            <div className='base_flex_row header_container'>
                <span className='header_no_click'>{get_current_window(headers)}</span>
                <button className='header_a' style={{
                    marginLeft: 'auto',
                    padding: '15px',
                    color: 'var(--header-current-text-color)',
                    backgroundColor: 'var(--header-color)',
                    boxShadow: 'none',
                }} onClick={() => set_mobile_show_view(!mobile_show_view)}>···</button>
                {mobile_show_view && <MobileHeaderView headers={headers} set_show={set_mobile_show_view}x/>}
            </div>
            ):(
            <div className='base_flex_row header_container'>
                {headers.map((header, i) => <Link key={i} to={header.path} style={{
                    backgroundColor: is_current_window(header.path) ? 'var(--header-current-color)': 'inherit',
                    color: is_current_window(header.path) ? 'var(--header-current-text-color)': 'var(--header-text-color)',
                    ...header.d_style,
                }} className='header_a'>{header.label}</Link>)}
                {theme === 'dark' ? (
                    <div className='header_a_theme base_flex_column' onClick={() => handle_theme('light')}>
                        <img src={light} alt="светлая тема" className='header_a_theme_icon'/>
                    </div>
                ) : (
                    <div className='header_a_theme base_flex_column' onClick={() => handle_theme('dark')}>
                        <img src={dark} alt="темная тема" className='header_a_theme_icon'/>
                    </div>
                )}
                {user.name === null || user.name === undefined ? (
                    <Link to='/auth/login' style={{
                        backgroundColor: is_current_window('/auth/login') ? 'var(--header-current-color)': 'inherit',
                        color: is_current_window('/auth/login') ? 'var(--header-current-text-color)': 'var(--header-text-color)',
                    }} className='header_a'>Вход</Link>
                ):(
                    <Link to='/auth/user' style={{
                        backgroundColor: is_current_window('/auth/user') ? 'var(--header-current-color)': 'inherit',
                        color: is_current_window('/auth/user') ? 'var(--header-current-text-color)': 'var(--header-text-color)',
                    }} className='header_a'>Профиль</Link>
                )}
            </div>
        )}
    </header>
}


export default CustomHeader;
