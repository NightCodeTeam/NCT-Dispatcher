import axios from "axios";


const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
})

// Интерцептор для добавления токена к запросам
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
            config.withCredentials = true;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Интерцептор для обработки ошибок авторизации
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401 || error.response?.status === 403) {
            localStorage.removeItem('token');
            window.location.href = '/auth/login';
        }
        return Promise.reject(error);
    }
);

export default api;