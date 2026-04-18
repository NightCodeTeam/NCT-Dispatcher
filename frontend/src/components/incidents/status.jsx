export const IncidentStatus = ({status}) => {
    return <div style={{
        userSelect: 'none',
        textAlign: "center",
        width: '100%',
        padding: '3px 10px',
        color: status === 'open'? 'rgba(248,26,26,0.91)': 'rgb(0,214,36)',
        backgroundColor: status === 'open'? 'rgba(39,0,0,0.88)': 'rgb(0,66,2)'
    }} className='rounded_border'>{status === 'open'? 'открыт': 'закрыт'}</div>
}


export default IncidentStatus;