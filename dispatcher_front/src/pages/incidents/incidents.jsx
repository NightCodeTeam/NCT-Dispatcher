import PaginationTable from "../../components/utils/custom_tables.jsx";
import incidents_service from "../../api/incidents.jsx";


const IncHead = () => {
    return <tr>
        <th>Название</th>
        <th style={{maxWidth: '50px', textAlign: 'center'}}>Приложение</th>
        <th style={{maxWidth: '50px'}}>Статус</th>
    </tr>
}


const IncDetails = ({data}) => {
    return <div className="overlay-backdrop">
        <div className="overlay-container">
            ssss
        </div>
    </div>
}


const IncLine = ({data, update, on_click}) => {
    const change_status = async () => {
        await incidents_service.update_incident(data.id, data.status === 'open' ? 'closed': 'open')
        update()
    }

    return <tr>
        <td onClick={() => on_click(data)}>{data.title}</td>
        <td style={{textAlign: "center", width: '100px'}}>{data.app_name}</td>
        <td onClick={() => change_status()} style={{
            textAlign: "center",
            width: '50px',
            padding: '3px 10px',
            color: data.status === 'open'? 'rgba(202,0,0,0.91)': 'rgb(0,214,36)',
            backgroundColor: data.status === 'open'? 'rgba(51,0,0,0.88)': 'rgb(0,66,2)'
        }} className='rounded_border'>{data.status === 'open'? 'открыт': 'закрыт'}</td>
    </tr>
}


const IncidentsView = () => {
    return <div style={{boxSizing: 'border-box'}}>
        <PaginationTable CustomHead={IncHead} Line={IncLine} Detail={IncDetails} api_request={incidents_service.all_incidents}/>
    </div>
}

export default IncidentsView;