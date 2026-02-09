import api from './main.jsx'


export const auth_service = {
    // Регистрация
    register: async (username, password, key) => {
        return (await api.post('/v1/auth/register', {
            name: username,
            password: password,
            key: key,
        })).data;
    },

    // Логин
    login: async (username, password) => {
        return (await api.post('/v1/auth/login', {
            name: username,
            password: password,
        })).data?.ok || false;
    },

    // Выход
    logout: async () => {
        await api.post('/v1/auth/logout')
        window.location.href = '/auth/login';
    },

    user: async () => {
        if (window.location.pathname.startsWith('/auth')){
            return ''
        }
        return await api.get('/v1/auth/who_am_i') || ''
    },

    // Проверка авторизации
    isAuthenticated: async () => {
        if (window.location.pathname.startsWith('/auth')) {
            return ''
        }
        return await api.get('/v1/auth/who_am_i') || ''
    },
};

export default auth_service;
