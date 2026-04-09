import { useState } from 'react'
import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import './css/style.css';

import {Login} from "./pages/auth/login.jsx";
import {Logout} from "./pages/auth/logout.jsx";
import {Register} from "./pages/auth/register.jsx";
import {AuthOutlet} from "./pages/auth/outlet.jsx";
import Dashboard from "./pages/dashboard.jsx";
import AppsView from "./pages/apps/apps.jsx";
import IncidentsView from "./pages/incidents/incidents.jsx";
import { useAuth } from "./components/auth/provider.jsx";


function App() {
    const [theme, set_theme] = useState(localStorage.getItem('theme') || 'dark');
    const {user, loading} = useAuth();

    if (user === '' && window.location.pathname !== '/auth/login') {
        window.location.href = '/auth/login';
    }

    return (
        <BrowserRouter>
            <div className='App' data-theme={theme}>
                <div>
                    <Routes>
                        <Route path="/" element={<Dashboard />}>
                            <Route path="" element={<IncidentsView />}/>
                            <Route path="apps" element={<AppsView />}/>
                        </Route>
                        <Route path="/auth" element={<AuthOutlet />}>
                            <Route path="login" element={<Login />}/>
                            <Route path="logout" element={<Logout />}/>
                            <Route path="register" element={<Register />}/>
                        </Route>
                    </Routes>
                </div>
            </div>
        </BrowserRouter>
    )
}

export default App
