import {Outlet} from 'react-router-dom';
import auth_service from "../../api/auth.jsx";


export const AuthOutlet = () => {
    if (window.location.pathname === '/auth') {
        if (!auth_service.isAuthenticated()) {
            window.location.href = '/auth/login';
        } else {
            window.location.href = '/';
        }
    }

    return <div className='full_screen' style={{height:'100dvh'}}>
        <Outlet />
    </div>
};
