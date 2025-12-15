import api from './main.jsx'


export const auth_service = {
    // Регистрация
    register: async (username, password, key) => {
        return (await api.post('/v1/auth/register', {
            username: username,
            password: password,
            key: key,
        })).data;
    },

    // Логин
    login: async (username, password) => {
        const response = await api.post('/v1/auth/login', {
            username: username,
            password: password,
        });

        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
            localStorage.setItem('name', username);
            return true;
        }
        return false;
    },

    // Выход
    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('name');
        window.location.href = '/auth/login';
    },

    user: () => {
        const username = localStorage.getItem('name')
        if (username === undefined || username === null) {
            window.location.href = '/auth/login';
        }
        return username
    },

    // Проверка авторизации
    isAuthenticated: () => {
        return !!localStorage.getItem('token');
    },
};

export default auth_service;