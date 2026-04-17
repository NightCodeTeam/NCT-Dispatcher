import { useState, useRef, useEffect } from 'react';


const SelectDropdown = ({ options = [10, 25, 50, 100], callback }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [selectedValue, setSelectedValue] = useState(options[0]);
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
        setSelectedValue(value);
        setIsOpen(false);
        // Здесь можно вызвать колбэк, если нужно передать значение родителю
        // onSelect && onSelect(value);
        callback(value);
    };

    return (
        <button className="select-dropdown" ref={dropdownRef}>
            <div
                className="select-header"
                onClick={() => setIsOpen(!isOpen)}
            >
                <span>{selectedValue}</span>
                <span className={`arrow ${isOpen ? 'open' : ''}`}>▼</span>
            </div>

            {isOpen && (
                <ul className="select-options">
                    {options.map((option) => (
                        <li
                            key={option}
                            className={`select-option ${selectedValue === option ? 'selected' : ''}`}
                            onClick={() => handleSelect(option)}
                        >
                            {option}
                        </li>
                    ))}
                </ul>
            )}
        </button>
    );
};

export default SelectDropdown;