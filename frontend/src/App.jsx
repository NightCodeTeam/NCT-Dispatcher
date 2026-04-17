import {
    BrowserRouter,
    Routes,
    Route, Navigate,
} from "react-router-dom";

import './css/style.css';
import {useTheme} from "@/context/theme.jsx"
import CustomHeader from "@/components/utils/custom_header.jsx";

import {LoginPage} from "@/pages/auth/login.jsx";
import {LogoutPage} from "@/pages/auth/logout.jsx";
import {RegisterPage} from "@/pages/auth/register.jsx";
import {AuthOutlet} from "@/pages/auth/outlet.jsx";
import {UserPage} from "@/pages/auth/user.jsx";

import AppsPage from "@/pages/apps.jsx";
import IncidentsPage from "@/pages/incidents.jsx";


function App() {
    const {theme} = useTheme();

    const headers = [
        {
            path: '/apps',
            label: 'Приложения',
        },
        {
            path: '/incidents',
            label: 'Инциденты'
        },
    ]

    return (
        <BrowserRouter>
            <div className='App' data-theme={theme}>
                <CustomHeader headers={headers}/>
                <Routes>
                    <Route path="/" element={<Navigate to={'/incidents'}/>}/>
                    <Route path="/apps" element={<AppsPage />}/>
                    <Route path="/incidents" element={<IncidentsPage />}/>
                    <Route path="/auth" element={<AuthOutlet />}>
                        <Route path="login" element={<LoginPage />}/>
                        <Route path="logout" element={<LogoutPage />}/>
                        <Route path="register" element={<RegisterPage />}/>
                        <Route path="user" element={<UserPage />}/>
                    </Route>
                </Routes>
            </div>
        </BrowserRouter>
    )
}

export default App
