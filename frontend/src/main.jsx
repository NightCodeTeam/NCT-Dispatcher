import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import {AuthProvider} from "./context/auth.jsx";
import {ThemeProvider} from "@/context/theme.jsx";

createRoot(document.getElementById('root')).render(
    <AuthProvider>
        <ThemeProvider>
            <App />
        </ThemeProvider>
    </AuthProvider>
)
