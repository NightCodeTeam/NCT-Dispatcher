import PropTypes from "prop-types";
import {useEffect, useState} from "react";
import IncidentsView from "../../pages/incidents/incidents.jsx";
import {LoadingAnimation} from "./loading_animation.jsx";


const PaginationTable = ({CustomHead, Line, Detail, api_request, adt_style}) => {
    const [show_detail, set_show_detail] = useState(false);
    const [detail_data, set_detail_data] = useState({});

    const [loading, set_loading] = useState(true);

    const [page, set_page] = useState(0);
    const [rows_per_page, set_rows_per_page] = useState(10);

    const [items, set_items] = useState([]);

    const handle_detail_data = (data) => {
        set_show_detail(true)
        set_detail_data(data)
    }

    const get_items = async () => {
        set_loading(true);
        set_show_detail(false)
        set_items(await api_request(page*rows_per_page, rows_per_page));
        set_loading(false);
    }

    const move_page = (add) => {
        if (add) {
            if (items.length === 0) {

            } else {
                set_page(page + 1);
            }
        } else {
            if (page === 0) {
                set_page(0)
            } else {
                set_page(page - 1);
            }
        }
    }

    useEffect(() => {
        get_items();
    }, []);

    useEffect(() => {
        get_items()
    }, [page, rows_per_page]);

    if (loading) {
        return <LoadingAnimation />
    }

    return <div style={{
        padding: 5,
        margin: '5px',
        ...adt_style,
    }} className='rounded_border'>
        <div style={{width:'100%'}} className='desktop'>
            <table style={{width:'100%'}}>
                <thead>
                <CustomHead />
                </thead>
                <tbody>
                {items.map((item, index) => (
                    <Line key={index} data={item} update={get_items} action_on_click={handle_detail_data}/>
                ))}
                </tbody>
            </table>
            <div className='base_flex_row' style={{
                flexWrap: 'nowrap',
                justifyContent: 'flex-start',
                alignItems: 'center'
            }}>
                <button onClick={() => move_page(false)} className='base_button' style={{
                    userSelect: 'none',
                }}>{'<'}</button>
                <span style={{userSelect: 'none'}}>{page + 1}</span>
                <button onClick={() => move_page(true)} className='base_button' style={{
                    userSelect: 'none',
                }}>{'>'}</button>
            </div>
        </div>
        <div style={{width:'100%'}} className='mobile'>
            <table style={{width:'100%'}}>
                <thead>
                <CustomHead />
                </thead>
                <tbody>
                {items.map((item, index) => (
                    <Line key={index} data={item} update={get_items} action_on_click={handle_detail_data}/>
                ))}
                </tbody>
            </table>
            <div className='base_flex_row' style={{
                flexWrap: 'nowrap',
                justifyContent: 'flex-start',
                alignItems: 'center'
            }}>
                <button onClick={() => move_page(false)} className='base_button' style={{
                    userSelect: 'none',
                }}>{'<'}</button>
                <span style={{userSelect: 'none'}}>{page + 1}</span>
                <button onClick={() => move_page(true)} className='base_button' style={{
                    userSelect: 'none',
                }}>{'>'}</button>
            </div>
        </div>
        {show_detail ? <Detail data={detail_data} on_close={() => set_show_detail(false)} update={get_items}/> : null}
    </div>
}
PaginationTable.propTypes = {
    CustomHead: PropTypes.element.isRequired,
    Line: PropTypes.element.isRequired,
    Detail: PropTypes.element.isRequired,
    api_request: PropTypes.func.isRequired,
    adt_style: PropTypes.object,
}


export default PaginationTable;