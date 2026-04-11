import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import './css/style.css';

import {Login} from "@/pages/auth/login.jsx";
import {Logout} from "@/pages/auth/logout.jsx";
import {Register} from "@/pages/auth/register.jsx";
import {AuthOutlet} from "@/pages/auth/outlet.jsx";
import Dashboard_old from "@/pages/dashboard_old.jsx";
import AppsView from "@/pages/apps/desktop.jsx";
import IncidentsView from "@/pages/incidents/incidents.jsx";
import {useTheme} from "@/context/theme.jsx"


function App() {
    const {theme} = useTheme();

    return (
        <BrowserRouter>
            <div className='App' data-theme={theme}>
                <div>
                    <Routes>
                        <Route path="/" element={<Dashboard_old />}>
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
