import {useEffect, useState} from "react";
import PaginationTable from "@/components/utils/custom_tables.jsx";
import back_service from "@/api/main.jsx";
import NewAppForm from "@/components/apps/new_form.jsx";
import useDevice from "@/context/mobile.jsx";
import {AppStatus} from "@/components/apps/status.jsx";
import AdtDataTable from "@/components/apps/adt_data.jsx";
import adt_data from "@/components/apps/adt_data.jsx";
import {AppChange} from "@/components/apps/change.jsx";


const AppHead = ({isMobile}) => {
    return <tr>
        <th style={{width: '20px'}}></th>
        <th style={{textAlign: 'left'}}>Название</th>
        <th style={{textAlign: 'right'}}>Инцидентов</th>
    </tr>
}


const AppLine = ({data, update, action_on_click, isMobile}) => {
    const handle_click = () => {
        action_on_click(data)
    }
    return <tr>
        <td style={{textAlign: 'right'}}><AppStatus status={data.status}/></td>
        {isMobile ? (
            <td style={{textAlign: 'left', height: '50px'}} onClick={() => handle_click()}>{data.name}</td>
        ) : <td style={{textAlign: 'left'}} onClick={() => handle_click()}>{data.name}</td>}
        <td style={{textAlign: 'right'}}>{data.incidents_count}</td>
    </tr>
}


const LogView = ({data}) => {
    const [extended, set_extended] = useState(false)
    return <div className='rounded_border' style={{
        padding: '5px',
        flex: 1,
        boxSizing: 'border-box',
        width: '100%',
    }}>
        <span onClick={() => set_extended(!extended)}><b>{data.title}</b> {extended ? '⯆': '⯈'}</span>
        {extended && <ul style={{
            color: 'rgba(174, 209, 243, 1)',
            backgroundColor: 'rgba(11, 20, 30, 1)',
            padding: "5px",
            marginBottom: '3px',
        }} className='rounded_border'>
            {data.log.split('\n').map((item, i) => <li key={i} style={{
                listStyle: 'none',
            }}><span style={{
                userSelect: 'none',
                color: 'rgba(174, 209, 243, 1)',
                backgroundColor: 'rgba(11, 20, 30, 1)',
            }}>{i}: </span>{item}</li>)}
        </ul>}
    </div>
}


const AppLogsData = ({data}) => {
    const [load, set_load] = useState(false)
    const [logs, set_logs] = useState([])

    const handle_download = async () => {
        set_logs(await back_service.apps.logs(data.id))
    }

    return <div className='rounded_border' style={{width:'100%'}}>
        {logs.length > 0 ? <div className='base_flex_column' style={{
                padding: '5px', boxSizing: 'border-box'
            }}>
            {logs.map((log, i) => <LogView key={i} data={log} />)}
            </div>:
            <div style={{padding: 5, maxWidth: '150px'}} onClick={() => handle_download()}>
                Скачать логи?
            </div>}
    </div>
}


const AppDetail = ({data, on_close, update}) => {
    const [new_data, set_new_data] = useState({
        name: data.name,
        status_url: data.status_url,
        status_code: data.status_code,
        logs_folder: data.logs_folder,
        script_path: data.script_path,
        new_code: false
    })
    const [change, set_change] = useState(false)

    const handle_change = (e) => {
        set_new_data({
            ...new_data,
            [e.target.name]: e.target.value,
        });
    }
    const change_app_submit = (e) => {
        e.preventDefault()
        console.log(new_data)
    }

    const handleOuterClick = () => {
        on_close();
    };

    const delete_app = async () => {
        await back_service.apps.del(data.id)
        update()
    }

    const handleInnerClick = (e) => {
        e.stopPropagation();
    };

    return <div className='overlay-backdrop' onClick={handleOuterClick}>
        <div className='overlay-content rounded_border base_flex_column' style={{
            alignItems: 'flex-start',
            padding: '5px'
        }} onClick={handleInnerClick}>
            <div className='base_flex_row' style={{
                justifyContent: 'space-between',
                width: '100%'
            }}>
                <div className='base_flex_row'>
                    <span><b>{data.name}</b></span>
                    <AppStatus status={data.status} />
                </div>
                <span onClick={() => navigator.clipboard.writeText(data.code)} style={{
                    color: 'rgba(174, 209, 243, 1)',
                    backgroundColor: 'rgba(11, 20, 30, 1)',
                    padding: "5px",
                    marginBottom: '3px',
                    cursor: 'pointer',
                }} className='rounded_border'>{data.code}</span>
            </div>
            <span>Процессор: {data.status.cpu_usage} %</span>
            <span>Память: {data.status.memory_usage} MB</span>
            <span>Диск: {data.status.disk_usage} %</span>
            <AdtDataTable data={data.status.adt_data}/>
            <span>{data.logs_folder}</span>
            <AppLogsData data={data}/>
            <div className='base_flex_row' style={{width: '100%', justifyContent: 'space-between'}}>
                <button onClick={() => set_change(!change)} style={{
                }} className='rounded_border'>Изменить</button>
                <button onClick={() => delete_app()} style={{
                }} className='rounded_border'>Удалить</button>
            </div>
            {change && (
                <AppChange formData={new_data} form_submit={change_app_submit} handleChange={handle_change}/>
            )}
        </div>
    </div>
}


const NewAppWindow = ({on_close}) => {
    const {isMobile} = useDevice()

    const [formData, setFormData] = useState({
        name: '',
        status_url: '',
        status_code: null,
        logs_folder: null,
        script_path: null,
    });

    const handleOuterClick = () => {
        on_close(false);
    };

    const handleInnerClick = (e) => {
        e.stopPropagation();
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const form_submit = async () => {
        if (formData.name !== '' && formData.status_url !== '') {
            await back_service.apps.new(formData)
        }
    }

    return <div className='overlay-backdrop' onClick={handleOuterClick}>
        <div className='overlay-content base_flex_column rounded_border' onClick={handleInnerClick} style={{
            minWidth: isMobile ? '85vw': '50vw',
            maxWidth: '90vw',
        }}>
            <NewAppForm formData={formData} form_submit={form_submit} handleChange={handleChange}/>
        </div>
    </div>
}


const AppsPage = () => {
    const [show_new, set_show_new] = useState(false);

    useEffect(() => {

    }, []);

    return <div style={{boxSizing: 'border-box', width: '100%', maxWidth: '50em', padding: 5}}>
        <button className='rounded_border base_margins' onClick={() => set_show_new(true)} style={{
            marginBottom: 5
        }}>Создать новое</button>
        <PaginationTable
            CustomHead={AppHead}
            Line={AppLine}
            Detail={AppDetail}
            api_request={back_service.apps.all}
        />
        {show_new && <NewAppWindow on_close={set_show_new}/>}
    </div>
}

export default AppsPage;
