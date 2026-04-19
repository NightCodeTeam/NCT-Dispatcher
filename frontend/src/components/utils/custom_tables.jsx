import { useEffect, useState } from "react";
import { useDevice } from "@/context/mobile.jsx";
import {LoadingAnimation, LoadingSimpleBlock} from "./loading_animation.jsx";
import SelectDropdown from "@/components/utils/select_dropdown.jsx";


const PaginationTable = ({ CustomHead, Line, Detail, api_request, adt_style }) => {
    const { isMobile } = useDevice();
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
        set_items(await api_request({
            skip: page*rows_per_page,
            limit: rows_per_page,
        }));
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
        get_items()
    }, [page, rows_per_page]);

    if (loading) {
        return <LoadingSimpleBlock />
    }

    return <div style={{
        padding: isMobile ? '0px' : '5px',
        borderWidth: isMobile ? '0px': '1px',
        ...adt_style,
    }} className='rounded_border'>
        <table style={{width:'100%'}}>
            <thead>
            <CustomHead isMobile={isMobile}/>
            </thead>
            <tbody>
            {items.map((item, index) => (
                <Line key={index} isMobile={isMobile} data={item} update={get_items} action_on_click={handle_detail_data}/>
            ))}
            </tbody>
        </table>
        <div className='base_flex_row no_wrap'>
            <button onClick={() => move_page(false)} style={{
                userSelect: 'none',
            }} disabled={page <= 0}>{'◀'}</button>
            <span style={{userSelect: 'none', padding: '0 5px'}}>{page + 1}</span>
            <button onClick={() => move_page(true)} style={{
                userSelect: 'none',
            }} disabled={items?.length < rows_per_page}>{'▶'}</button>
            <SelectDropdown callback={set_rows_per_page} selected={rows_per_page}/>
        </div>
        {show_detail ? <Detail data={detail_data} isMobile={isMobile} on_close={() => set_show_detail(false)} update={get_items}/> : null}
    </div>
}


export default PaginationTable;
