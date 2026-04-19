import axios from "axios";

axios.defaults.withCredentials = true;


const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true
})

// Флаг, чтобы не спамить редиректами, если несколько запросов упали одновременно
let isRedirecting = false;

// Интерцептор для обработки ошибок авторизации
api.interceptors.response.use(
    (response) => response,
    (error) => {
        const isNetworkError = !error.response;
        const isServerError = error.response && error.response.status >= 500;
        if ((isNetworkError || isServerError) && !isRedirecting) {
              isRedirecting = true;

              if (!window.location.pathname.includes('/error')) {
                window.location.href = '/auth/login';
              } else {
                isRedirecting = false; // Сброс, если мы уже на странице ошибки
              }
            }

        if (error.response?.status === 401 || error.response?.status === 405) {
            window.location.href = '/auth/login';
        }
        if (error.response?.status === 403) {
            window.location.href = '/auth/login';
        }
        if (error.response?.status === 403) {
            window.location.href = '/auth/login';
        }
        return Promise.reject(error);
    }
);

export default api;
