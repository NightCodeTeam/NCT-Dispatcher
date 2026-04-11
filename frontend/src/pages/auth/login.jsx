import { useState } from 'react';
import {Link, useNavigate} from "react-router-dom"
import {LoadingAnimation} from "@/components/utils/loading_animation.jsx";
import {useAuth} from "@/context/auth.jsx";


export const LoginPage = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const {login} = useAuth()

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await login(formData.username, formData.password)

            navigate('/')
        } catch (error) {
            console.log(error)
            setError(error.response?.data?.detail || 'Непредвиденная ошибка');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <LoadingAnimation />
    }

    return <form onSubmit={handleSubmit} className='base_flex_column'>
        <input
            type="text"
            name="username"
            placeholder="Логин"
            className='base_button'
            style={{
                textAlign: 'center',
            }}
            value={formData.username}
            onChange={handleChange}
            required
        />
        <input
            type="password"
            name="password"
            placeholder="Пароль"
            className='base_button'
            style={{
                textAlign: 'center',
            }}
            value={formData.password}
            onChange={handleChange}
            required
        />
        {error && <div style={{ color: 'red' }}>{error}</div>}
        <button type="submit" disabled={loading} className='base_button desktop'>
            {loading ? 'Вхожу...' : 'Войти'}
        </button>
        <button type="submit" disabled={loading} style={{
            padding: '15px',
            marginTop: '10px',
        }} className='base_button mobile'>
            {loading ? 'Вхожу...' : 'Войти'}
        </button>
        <Link to='/auth/register' style={{
            textDecoration: 'none',
            userSelect: 'none',
        }} className='desktop'>Создать</Link>
        <Link to='/auth/register' style={{
            textDecoration: 'none',
            userSelect: 'none',
            marginTop: 10
        }} className='mobile'>Создать</Link>
    </form>
};
