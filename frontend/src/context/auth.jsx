import { createContext, useState, useEffect, useContext } from 'react';
import auth_service from '@/api/auth.jsx';
import {LoadingAnimation} from "@/components/utils/loading_animation.jsx";


const AuthContext = createContext({});


export function AuthProvider({ children }) {
    const [user, set_user] = useState({
        name: null
    });
    const [loading, set_loading] = useState(true);

    const check_auth = async () => {
        try {
            set_loading(true);
            const new_user = await auth_service.user()
            set_user({name: new_user.name })
        } catch (error) {
            if (error.status === 401) {
                set_user(prev => ({ ...prev, name: null }))
            }
        } finally {
            set_loading(false);
        }
    };

    useEffect(() => {
        check_auth();
    }, []);

    const login = async (name, password) => {
        set_loading(true);
        const data = await auth_service.login(name, password);
        set_user({ name: data.name })
        set_loading(false);
    };

    const logout = async () => {
        set_loading(true);
        await auth_service.logout();
        set_user({ name: null })
        set_loading(false);
    };

    if (loading) {
        return <LoadingAnimation />
    }

    return (
        <AuthContext.Provider value={{
            user,
            login,
            logout,
            loading,
            check_auth
        }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);
