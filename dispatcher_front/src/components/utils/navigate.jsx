import PropTypes from "prop-types";
import {useNavigate} from "react-router-dom";


export const NavigateButton = ({inner, nav_to, adt_style}) => {
    const navigate = useNavigate();
    const style ={
        ...adt_style
    }

    const onClick = (e) => {
        //e.preventDefault()
        navigate(nav_to)
    }

    return (
        <button onClick={(e) => (onClick(e))} style={style} className='base_button'>{inner}</button>
    )
}
NavigateButton.propTypes = {
    inner: PropTypes.oneOfType([PropTypes.func, PropTypes.object, PropTypes.string, PropTypes.number, PropTypes.element]).isRequired,
    nav_to: PropTypes.string.isRequired,
    adt_style: PropTypes.object
}