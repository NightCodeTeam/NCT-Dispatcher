import {useState} from "react";
import PaginationTable from "@/components/utils/custom_tables.jsx";
import apps_service from "@/api/apps.jsx";
import back_service from "@/api/main.jsx";
import NewAppForm from "@/components/apps/new_form.jsx";
import useDevice from "@/context/mobile.jsx";


const AppHead = () => {
    return <tr>
        <th style={{textAlign: 'left'}}>Название</th>
        <th style={{textAlign: 'right'}}>Инцидентов</th>
    </tr>
}


const AppLine = ({data, update, action_on_click}) => {
    const handle_click = () => {
        action_on_click(data)
    }
    return <tr>
        <td className='desktop' style={{textAlign: 'left'}} onClick={() => handle_click()}>{data.name}</td>
        <td className='mobile' style={{textAlign: 'left', height: '50px'}} onClick={() => handle_click()}>{data.name}</td>
        <td style={{textAlign: 'right'}}>{data.incidents.length}</td>
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
        set_logs(await apps_service.app_logs(data.id))
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
    const handleOuterClick = () => {
        on_close();
    };

    const delete_app = async () => {
        await apps_service.del_app(data.id)
        update()
    }

    const handleInnerClick = (e) => {
        e.stopPropagation();
    };

    return <div className='overlay-backdrop' onClick={handleOuterClick}>
        <div className='desktop overlay-content rounded_border' onClick={handleInnerClick}>
            <div className='base_flex_column' style={{
                alignItems: 'flex-start',
                padding: '5px',
                width: '50em'
            }}>
                <span><b>{data.name}</b></span>
                <span onClick={() => navigator.clipboard.writeText(data.code)} style={{
                    color: 'rgba(174, 209, 243, 1)',
                    backgroundColor: 'rgba(11, 20, 30, 1)',
                    padding: "5px",
                    marginBottom: '3px',
                    cursor: 'pointer',
                }} className='rounded_border'>{data.code}</span>
                <spa>{data.logs_folder}</spa>
                <AppLogsData data={data}/>
                <button onClick={() => delete_app()} style={{
                    marginLeft: 'auto',
                    marginRight: '5',
                    right: '5'
                }} className='rounded_border'>Удалить</button>
            </div>
        </div>
        <div className='mobile' onClick={handleInnerClick} style={{
            marginTop: '50px',
            padding: '5px',
        }}>
            <div className='base_flex_column' style={{
                alignItems: 'flex-start',
            }}>
                <span><b>{data.name}</b></span>
                <span onClick={() => navigator.clipboard.writeText(data.code)} style={{
                    color: 'rgba(174, 209, 243, 1)',
                    backgroundColor: 'rgba(11, 20, 30, 1)',
                    padding: "5px",
                    marginBottom: '3px',
                    cursor: 'pointer',
                }} className='rounded_border'>{data.code}</span>
                <spa>{data.logs_folder}</spa>
                <AppLogsData data={data}/>
                <button onClick={() => delete_app()} style={{
                    marginLeft: 'auto',
                    marginRight: '5',
                    right: '5'
                }} className='rounded_border'>Удалить</button>
            </div>
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
        script: null,
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
        {isMobile ? (
            <div className='overlay-content base_flex_column rounded_border' onClick={handleInnerClick} style={{
                minWidth: '85vw',
                maxWidth: '90vw',
            }}>
                <NewAppForm formData={formData} form_submit={form_submit} handleChange={handleChange}/>
            </div>
        ):(
            <div className='overlay-content base_flex_column rounded_border' onClick={handleInnerClick} style={{
                minWidth: '50vw',
                maxWidth: '90vw',
            }}>
                <NewAppForm formData={formData} form_submit={form_submit} handleChange={handleChange}/>
            </div>
        )}
    </div>
}


const AppsView = () => {
    const [show_new, set_show_new] = useState(false);

    return <div style={{boxSizing: 'border-box'}}>
        <PaginationTable CustomHead={AppHead} Line={AppLine} Detail={AppDetail} api_request={apps_service.all_apps}/>
        {show_new && <NewAppWindow on_close={set_show_new}/>}
        <button className='rounded_border base_margins' onClick={() => set_show_new(true)} style={{
            marginTop: 0
        }}>Создать новое</button>
    </div>
}

export default AppsView;