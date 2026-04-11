import { useEffect } from "react";
import { useAuth } from "@/context/auth.jsx";


export const LogoutPage = () => {
    const {logout} = useAuth()

    const handleLogout = async () => {
        await logout();
    }

    useEffect(() => {
        handleLogout();
    }, []);

    return <div>Всего хорошего!</div>
}
