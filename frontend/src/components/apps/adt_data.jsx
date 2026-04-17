const AdtDataTable = ({data}) => {
    const columns = (data !== undefined && data !== null) ? Object.keys(data): []

    const formatValue = (value) => {
        if (value === null || value === undefined) {
            return '—';
        }
        if (typeof value === 'object') {
            return JSON.stringify(value);
        }
        if (typeof value === 'boolean') {
            return value ? 'Да' : 'Нет';
        }
        return String(value);
    };

    const formatHeader = (header) => {
        return header.charAt(0).toUpperCase() + header.slice(1).replace(/_/g, ' ');
    };

    if (data === undefined || data === null) {
        return <div>Нет дополнительных данных</div>;
    }

    return <div>
        <h4 style={{
            margin: 0
        }}>Дополнительные данные:</h4>
        <div style={{ overflowX: 'auto' }}>
            <table style={{
                width: '100%',
                borderCollapse: 'collapse',
                backgroundColor: 'white',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)'}}><tbody>
            {Object.entries(data).map((item, index) => (
                <tr key={index} style={{

                }}>
                    <td>{formatHeader(item[0])}</td>
                    <td>{formatValue(item[1])}</td>
                </tr>
            ))}
            </tbody></table>
        </div>
    </div>
};

export default AdtDataTable;