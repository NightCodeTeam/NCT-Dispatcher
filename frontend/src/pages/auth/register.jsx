import { useState } from 'react';
import { auth_service } from '../../api/auth';
import {LoadingAnimation} from "../../components/utils/loading_animation.jsx";
import {
    Link,
    useNavigate,
} from "react-router-dom"


export const Register = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        confirmPassword: '',
        key: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

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

        if (formData.username.length < 6 || formData.password.length < 6) {
            setError('Пароль или имя пользователя меньше 6 символов')
            setLoading(false);
            return;
        }

        if (formData.password !== formData.confirmPassword) {
            setError('Пароли не совпадают');
            setLoading(false);
            return;
        }

        try {
            const res = await auth_service.register(formData.username, formData.password, formData.key);
            if (res.ok === true) {
                navigate('/auth/login')
            }
        } catch (error) {
            setError(error.response?.data?.detail || 'Регистрация не удалась');
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
        <input
            type="password"
            name="confirmPassword"
            placeholder="Повтор пароля"
            className='base_button'
            style={{
                textAlign: 'center',
            }}
            value={formData.confirmPassword}
            onChange={handleChange}
            required
        />
        <input
            type="text"
            name="key"
            placeholder="Ключ"
            className='base_button'
            style={{
                textAlign: 'center',
            }}
            value={formData.key}
            onChange={handleChange}
            required
        />
        {error && <div style={{ color: 'red' }}>{error}</div>}
        <button type="submit" disabled={loading} className='base_button desktop'>
            {loading ? 'Регистрируюсь...' : 'Регистрация'}
        </button>
        <button type="submit" disabled={loading} style={{
            padding: '15px',
            marginTop: '10px',
        }} className='base_button mobile'>
            {loading ? 'Регистрируюсь...' : 'Регистрация'}
        </button>
        <Link to='/auth/login' style={{
            textDecoration: 'none',
            userSelect: 'none',
        }} className='desktop'>Есть аккаунт</Link>
        <Link to='/auth/login' style={{
            textDecoration: 'none',
            userSelect: 'none',
            marginTop: 10
        }} className='mobile'>Есть аккаунт</Link>
        {import.meta.env.VITE_DEBUG && (
            <div>
                В режиме разработки используйте ключ "123" для регистрации.
            </div>
        )}
    </form>
};
