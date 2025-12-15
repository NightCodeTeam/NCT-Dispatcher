import incidents_service from "../../api/incidents.jsx";
import {not_to_long_text} from "../../components/utils/string_line.jsx";
import PaginationTable from "../../components/utils/custom_tables.jsx";


function get_level(data) {
    if (data.level === 'debug') {
        return {
            label: 'ДЕБАГ',
            color: 'rgb(0,112,27)',
            background: 'rgb(0,255,61)',
        }
    }
    if (data.level === 'info') {
        return {
            label: 'ИНФО',
            color: 'rgb(0,255,185)',
            background: 'rgb(0,158,109)',
        }
    }
    if (data.level === 'warning') {
        return {
            label: 'ВНИМАНИЕ',
            color: 'rgb(159,106,1)',
            background: 'rgb(255,212,0)',
        }
    }
    if (data.level === 'error') {
        return {
            label: 'ОШИБКА',
            color: 'rgb(255,0,0)',
            background: 'rgb(255,167,0)',
        }
    }
    if (data.level === 'crit') {
        return {
            label: 'КРИТ',
            color: 'rgb(255,0,0)',
            background: 'rgba(1, 1, 1, 1)',
        }
    }
}


const IncHead = () => {
    return <tr>
        <th style={{textAlign: 'left'}}>Название</th>
        <th className='desktop' style={{maxWidth: '50px', textAlign: 'center'}}>Приложение</th>
        <th className='desktop' style={{maxWidth: '50px'}}>Уровень</th>
        <th className='mobile' style={{padding: 0}}>Приложение Уровень</th>
        <th style={{maxWidth: '50px'}}>Статус</th>
    </tr>
}


const IncDetails = ({data, on_close, update}) => {
    const date = new Date(data.created_at);

    const change_status = async () => {
        await incidents_service.update_incident(data.id, data.status === 'open' ? 'closed': 'open')
        update()
    }

    const delete_inc = async () => {
        await incidents_service.del_incident(data.id)
        update()
    }

    const handleOuterClick = () => {
        on_close();
    };

    const handleInnerClick = (e) => {
        e.stopPropagation(); // Останавливаем всплытие события
    };

    return <div className="overlay-backdrop" onClick={() => handleOuterClick()}>
        <div className="overlay-content base_flex_column rounded_border base_margins desktop" style={{
            width: '50em',
        }} onClick={(e) => handleInnerClick(e)}>
            <div className='base_flex_row' style={{flexWrap: 'nowrap', justifyContent: 'space-between', width: '100%'}}>
                <span><b>{data.title}</b></span>
                <span>{date.toLocaleString('ru-Ru')}</span>
                <span onClick={() => change_status()} style={{
                    userSelect: 'none',
                    textAlign: "center",
                    width: '50px',
                    padding: '3px 10px',
                    color: data.status === 'open'? 'rgba(248,26,26,0.91)': 'rgb(0,214,36)',
                    backgroundColor: data.status === 'open'? 'rgba(39,0,0,0.88)': 'rgb(0,66,2)'
                }} className='rounded_border'>{data.status === 'open'? 'открыт': 'закрыт'}</span>
            </div>
            <div className='base_flex_row' style={{flexWrap: 'nowrap', justifyContent: 'flex-start', width: '100%'}}>
                <span><b>{data.app_name}</b></span>
                <span style={{
                    userSelect: 'none',
                    textAlign: "center",
                    padding: '3px 10px',
                    color: get_level(data).color,
                    borderColor: get_level(data).color,
                    backgroundColor: get_level(data).background,
                    fontWeight: 'bolder',
                }} className='rounded_border'>{get_level(data).label}</span>
            </div>
            <div>
                <div style={{whiteSpace: 'pre-wrap'}}>{data.message}</div>
                <ul style={{
                    color: 'rgba(174, 209, 243, 1)',
                    backgroundColor: 'rgba(11, 20, 30, 1)',
                    padding: "5px",
                    marginBottom: '3px',
                }} className='rounded_border'>
                    {data.logs.split('\n').map((item, i) => <li key={i}>{i}: {item}</li>)}
                </ul>
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
        <div className="base_flex_column mobile" style={{
            width: '100%',
            marginTop: '50px',
            borderWidth: '0px',
        }} onClick={(e) => handleInnerClick(e)}>
            <div className='base_flex_row' style={{flexWrap: 'nowrap', justifyContent: 'space-between', width: '100%'}}>
                <span><b>{data.title}</b></span>
                <span>{date.toLocaleString('ru-Ru')}</span>
                <span onClick={() => change_status()} style={{
                    userSelect: 'none',
                    textAlign: "center",
                    width: '50px',
                    padding: '3px 10px',
                    color: data.status === 'open'? 'rgba(248,26,26,0.91)': 'rgb(0,214,36)',
                    backgroundColor: data.status === 'open'? 'rgba(39,0,0,0.88)': 'rgb(0,66,2)'
                }} className='rounded_border'>{data.status === 'open'? 'открыт': 'закрыт'}</span>
            </div>
            <div className='base_flex_row' style={{flexWrap: 'nowrap', justifyContent: 'flex-start', width: '100%'}}>
                <span><b>{data.app_name}</b></span>
                <span style={{
                    userSelect: 'none',
                    textAlign: "center",
                    padding: '3px 10px',
                    color: get_level(data).color,
                    borderColor: get_level(data).color,
                    backgroundColor: get_level(data).background,
                    fontWeight: 'bolder',
                }} className='rounded_border'>{get_level(data).label}</span>
            </div>
            <div>
                <div style={{whiteSpace: 'pre-wrap'}}>{data.message}</div>
                <ul style={{
                    color: 'rgba(174, 209, 243, 1)',
                    backgroundColor: 'rgba(11, 20, 30, 1)',
                    padding: "5px",
                    marginBottom: '3px',
                }}>
                    {data.logs.split('\n').map((item, i) => <li key={i}>{i}: {item}</li>)}
                </ul>
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


const IncLine = ({data, update, action_on_click}) => {
    const change_status = async () => {
        await incidents_service.update_incident(data.id, data.status === 'open' ? 'closed': 'open')
        update()
    }

    const handle_click = () => {
        action_on_click(data)
    }

    return <tr>
        <td className='desktop' onClick={() => handle_click()} dangerouslySetInnerHTML={{__html: not_to_long_text(data.title, data.message, 150)}}></td>
        <td className='mobile' onClick={() => handle_click()} dangerouslySetInnerHTML={{__html: not_to_long_text(data.title, data.message, 50)}}></td>
        <td className='desktop' style={{textAlign: "center", width: '100px'}} onClick={() => handle_click()}>{data.app_name}</td>
        <td className='rounded_border desktop' style={{
            userSelect: 'none',
            textAlign: "center",
            padding: '3px 10px',
            color: get_level(data).color,
            borderColor: get_level(data).color,
            backgroundColor: get_level(data).background,
            fontWeight: 'bolder',
        }} onClick={() => handle_click()}>{get_level(data).label}</td>
        <td className='mobile base_flex_column'>
            <span>{data.app_name}</span>
            <span style={{
                userSelect: 'none',
                textAlign: "center",
                padding: '3px 10px',
                color: get_level(data).color,
                borderColor: get_level(data).color,
                backgroundColor: get_level(data).background,
                fontWeight: 'bolder',
            }} className='rounded_border' onClick={() => handle_click()}>{get_level(data).label}</span>
        </td>
        <td onClick={() => change_status()} style={{
            userSelect: 'none',
            textAlign: "center",
            width: '50px',
            padding: '3px 10px',
            color: data.status === 'open'? 'rgba(248,26,26,0.91)': 'rgb(0,214,36)',
            backgroundColor: data.status === 'open'? 'rgba(39,0,0,0.88)': 'rgb(0,66,2)'
        }} className='rounded_border'>{data.status === 'open'? 'открыт': 'закрыт'}</td>
    </tr>
}


const IncidentsView = () => {
    return <div style={{boxSizing: 'border-box'}}>
        <PaginationTable CustomHead={IncHead} Line={IncLine} Detail={IncDetails} api_request={incidents_service.all_incidents}/>
    </div>
}

export default IncidentsView;