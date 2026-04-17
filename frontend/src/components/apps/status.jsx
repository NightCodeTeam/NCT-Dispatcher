export const AppStatus = ({status, compact = true}) => {
    if (compact) {
        return <div className="rounded_border" style={{
            backgroundColor: status.ok ? 'green' : 'red',
            width: '15px',
            height: '15px',
            margin: "auto 1px auto auto"
        }}></div>
    }
};
