import { useEffect } from "react";
import auth_service from "../../api/auth.jsx";

export const Logout = ({set_username}) => {

        const handletest = async () => {
            await auth_service.logout()
            set_username('')
        }

        useEffect(() => {
            handletest();
        }, []);

    return <div>Всего хорошего!</div>
}
