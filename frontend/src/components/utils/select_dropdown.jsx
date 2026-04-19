import { useState, useRef, useEffect } from 'react';


const SelectDropdown = ({ options = [10, 25, 50, 100], selected, callback }) => {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    // Закрытие по клику вне компонента
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleSelect = (value) => {
        setIsOpen(false);
        // Здесь можно вызвать колбэк, если нужно передать значение родителю
        // onSelect && onSelect(value);
        callback(value);
    };

    return <button
        className="select-dropdown"
        ref={dropdownRef}
        onClick={() => setIsOpen(!isOpen)}
    >
        <div className="base_flex_row no_wrap space-between">
            <span>{selected}</span>
            <span className={`arrow ${isOpen ? 'open' : ''}`}>▼</span>
        </div>
        {isOpen && (
            <ul className="select-options">
                {options.map((option) => (
                    <li
                        key={option}
                        className={`select-option ${selected === option ? 'selected' : ''}`}
                        onClick={() => handleSelect(option)}
                    >
                        {option}
                    </li>
                ))}
            </ul>
        )}
    </button>
};

export default SelectDropdown;