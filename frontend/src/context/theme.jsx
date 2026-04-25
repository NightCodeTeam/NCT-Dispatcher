import { createContext, useState, useContext } from 'react';


const ThemeContext = createContext({});


export function ThemeProvider({ children }) {
    const [theme, setTheme] = useState(get_theme());

    function get_theme() {
        const them = localStorage.getItem('theme')
        if (them === null || them === undefined) {
            set_theme('dark')
            return 'dark'
        }
        return them;
    }

    function set_theme(theme) {
        setTheme(theme);
        localStorage.setItem('theme', theme);
    }

    return (
        <ThemeContext.Provider value={{
            theme,
            set_theme
        }}>
            {children}
        </ThemeContext.Provider>
    );
};

export const useTheme = () => useContext(ThemeContext);
