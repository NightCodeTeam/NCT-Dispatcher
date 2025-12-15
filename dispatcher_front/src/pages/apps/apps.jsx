import {useState} from "react";
import PaginationTable from "../../components/utils/custom_tables.jsx";
import apps_service from "../../api/apps.jsx";


const AppHead = () => {
    return <tr>
        <th style={{textAlign: 'left'}}>Название</th>
        <th style={{textAlign: 'right'}}>Кол-во инцидентов</th>
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
    const [new_name, set_name] = useState('');
    const [new_status, set_status] = useState('');
    const [new_folder, set_folder] = useState('');

    const handleOuterClick = () => {
        on_close(false);
    };

    const handleInnerClick = (e) => {
        e.stopPropagation();
    };

    const form_submit = async () => {
        await apps_service.new_app(
            new_name,
            new_status,
            new_folder,
        )
    }

    return <div className='overlay-backdrop' onClick={handleOuterClick}>
        <div className='overlay-content base_flex_column rounded_border base_margins desktop' onClick={handleInnerClick}>
            <form className='base_flex_column' onSubmit={() => form_submit()} style={{
                maxWidth: '50em',
                padding: '5px',
                alignItems: 'flex-start',
            }}>
                <input type='text' style={{padding: 5, width: '30em'}} className='rounded_border' placeholder='Название' value={new_name} onChange={(e) => set_name(e.target.value)}/>
                <input type='text' style={{padding: 5, width: '30em'}} className='rounded_border' placeholder='Статус URL' value={new_status} onChange={(e) => set_status(e.target.value)}/>
                <input type='text' style={{padding: 5, width: '30em'}} className='rounded_border' placeholder='Папка логов (полный путь)' value={new_folder} onChange={(e) => set_folder(e.target.value)}/>
                <input type='submit' style={{padding: 5}} className='rounded_border' value='Создать'/>
            </form>
        </div>
        <div className='mobile' style={{
            marginTop: '50px',
            padding: '5px 0',
            boxSizing: 'border-box',
        }} onClick={handleInnerClick}>
            <form className='base_flex_column' onSubmit={() => form_submit()} style={{
                width: '100%',
                alignItems: 'flex-start',
            }}>
                <input type='text' style={{padding: 5, width: '100%'}} className='rounded_border' placeholder='Название' value={new_name} onChange={(e) => set_name(e.target.value)}/>
                <input type='text' style={{padding: 5, width: '100%'}} className='rounded_border' placeholder='Статус URL' value={new_status} onChange={(e) => set_status(e.target.value)}/>
                <input type='text' style={{padding: 5, width: '100%'}} className='rounded_border' placeholder='Папка логов (полный путь)' value={new_folder} onChange={(e) => set_folder(e.target.value)}/>
                <input type='submit' style={{padding: 5}} className='rounded_border' value='Создать'/>
            </form>
        </div>
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