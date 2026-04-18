import back_service from "@/api/main.jsx";
import {not_to_long_text} from "@/components/utils/string_line.jsx";
import PaginationTable from "@/components/utils/custom_tables.jsx";
import IncidentLevel from "@/components/incidents/level.jsx";
import IncidentStatus from "@/components/incidents/status.jsx";


const IncHead = ({isMobile}) => {
    return <tr>
        <th style={{textAlign: 'left'}}>Название</th>
        {isMobile && (
            <th style={{padding: 0}}>Приложение Уровень</th>
        )}
        {!isMobile && (
            <th style={{maxWidth: '50px', textAlign: 'center'}}>Приложение</th>
        )}
        {!isMobile && (
            <th style={{maxWidth: '50px'}}>Уровень</th>
        )}
        <th style={{maxWidth: '50px'}}>Статус</th>
    </tr>
}


const IncDetails = ({isMobile, data, on_close, update}) => {
    const date = new Date(data.created_at);
    const logs = data.logs !== undefined && data.logs !== '' ? data.logs.split('\n') : [];

    const change_status = async () => {
        await back_service.incidents.update({
            incident_id: data.id,
            new_status: data.status === 'open' ? 'closed' : 'open'
        })
        update()
    }

    const delete_inc = async () => {
        await back_service.incidents.del(data.id)
        update()
    }

    const handleOuterClick = () => {
        on_close();
    };

    const handleInnerClick = (e) => {
        e.stopPropagation(); // Останавливаем всплытие события
    };

    return <div className="overlay-backdrop" onClick={handleOuterClick}>
        <div className="overlay-content base_flex_column rounded_border no_wrap" style={{
            padding: '5px'
        }} onClick={(e) => handleInnerClick(e)}>
            <div className='base_flex_row' style={{flexWrap: isMobile ? 'wrap': 'nowrap', justifyContent: 'space-between', width: '100%'}}>
                <span><b>{data.title}</b></span>
                <span>{date.toLocaleString('ru-Ru')}</span>
                <IncidentLevel level={data.level}/>
            </div>
            <div className='base_flex_column no_wrap'>
                <div style={{whiteSpace: 'pre-wrap'}}>{data.message}</div>
                {logs.length > 0 && <ul style={{
                    width: '100%',
                    color: 'rgba(174, 209, 243, 1)',
                    backgroundColor: 'rgba(11, 20, 30, 1)',
                    marginBottom: '3px',
                }} className='rounded_border'>
                    {logs.map((item, i) => <li key={i}>{i}: {item}</li>)}
                </ul>}
            </div>
            <div className='base_flex_row' style={{flexWrap: 'nowrap', justifyContent: 'space-between'}}>
                {data.status === 'closed' && <button onClick={() => delete_inc()} style={{

                }} className='base_button'>Удалить</button>}
                {data.edit_by_user !== null && data.edit_by_user !== undefined ? <div className='base_flex_row'>
                    <span>{data.edit_by_user}</span>
                    <span>({new Date(data.updated_at).toLocaleString('ru-RU')})</span>
                </div>: null}
            </div>
        </div>
    </div>
}


const IncLine = ({isMobile, data, update, action_on_click}) => {
    const change_status = async () => {
        await back_service.incidents.update({
            incident_id: data.id,
            new_status: data.status === 'open' ? 'closed' : 'open'
        })
        update()
    }

    const handle_click = () => {
        action_on_click(data)
    }

    return <tr>
        <td onClick={() => handle_click()} dangerouslySetInnerHTML={{__html: not_to_long_text(data.title, data.message, isMobile ? 50: 150)}}></td>
        {isMobile && (
            <td className='mobile base_flex_column'>
                <span>{data.app_name}</span>
                <IncidentLevel level={data.level}/>
            </td>
        )}
        {!isMobile && (
            <td className='desktop' style={{textAlign: "center", width: '100px'}} onClick={() => handle_click()}>{data.app_name}</td>
        )}
        {!isMobile && (
            <td><IncidentLevel level={data.level}/></td>
        )}
        <td onClick={() => change_status()} style={{
            width: '75px',
        }}><IncidentStatus status={data.status} /></td>
    </tr>
}


const IncidentsPage = () => {
    return <div style={{width: '100%', maxWidth: '50em', padding: 5}}>
        <PaginationTable CustomHead={IncHead} Line={IncLine} Detail={IncDetails} api_request={back_service.incidents.all}/>
    </div>
}

export default IncidentsPage;