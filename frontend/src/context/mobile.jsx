import {useEffect, useState} from "react";


export const useDevice = () => {
    const [state, setState] = useState({
        isMobile: false,
        isCoarse: false
    });

    useEffect(() => {
        // Проверяем, что мы в браузере
        if (typeof window === 'undefined') return;

        // Создаем media query объекты
        const mobileQuery = window.matchMedia('(max-width: 768px)');
        const coarseQuery = window.matchMedia('(pointer: coarse)');

        // Функция обновления состояния
        const updateState = () => {
            setState({
                isMobile: mobileQuery.matches,
                isCoarse: coarseQuery.matches
            });
        };

        // Устанавливаем начальное значение
        updateState();

        // Подписываемся на изменения
        // Используем современный addEventListener если доступен, иначе fallback
        if (mobileQuery.addEventListener) {
            mobileQuery.addEventListener('change', updateState);
            coarseQuery.addEventListener('change', updateState);
        } else {
            // Fallback для старых браузеров
            mobileQuery.addListener(updateState);
            coarseQuery.addListener(updateState);
        }

        // Отписываемся при размонтировании
        return () => {
            if (mobileQuery.removeEventListener) {
                mobileQuery.removeEventListener('change', updateState);
                coarseQuery.removeEventListener('change', updateState);
            } else {
                mobileQuery.removeListener(updateState);
                coarseQuery.removeListener(updateState);
            }
        };
    }, []);

    return state;
};

export default useDevice;