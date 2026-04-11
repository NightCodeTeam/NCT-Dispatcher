import { createContext, useState, useEffect, useContext } from 'react';
import auth_service from '@/api/auth.jsx';


const AuthContext = createContext({});


export function AuthProvider({ children }) {
    const [user, set_user] = useState({
        name: null
    });
    const [loading, set_loading] = useState(true);

    const check_auth = async () => {
        try {
            set_user(await auth_service.user())
        } catch (error) {
            if (error.status === 401) {
                set_user({name: null});
            }
        } finally {
            set_loading(false);
        }
    };

    useEffect(() => {
        check_auth();
    }, []);

    const login = async (name, password) => {
        const data = await auth_service.login(name, password);
        set_user(data)
    };

    const logout = async () => {
        await auth_service.logout();
        set_user(null);
    };

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
