import { useAuth } from '@/context/auth.jsx'


export const UserPage = () => {
    const { user, logout } = useAuth()

    return <div className='base_flex_column no_wrap'>
        <span className='no_select'>Имя: </span><span>{user.name}</span>
        <button onClick={logout}>Выйти</button>
    </div>
};
