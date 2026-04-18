function get_level(level) {
    if (level === 'debug') {
        return {
            label: 'ДЕБАГ',
            color: 'rgb(0,112,27)',
            background: 'rgb(0,255,61)',
        }
    }
    if (level === 'info') {
        return {
            label: 'ИНФО',
            color: 'rgb(0,255,185)',
            background: 'rgb(0,158,109)',
        }
    }
    if (level === 'warning') {
        return {
            label: 'ВНИМАНИЕ',
            color: 'rgb(159,106,1)',
            background: 'rgb(255,212,0)',
        }
    }
    if (level === 'error') {
        return {
            label: 'ОШИБКА',
            color: 'rgb(255,0,0)',
            background: 'rgb(255,167,0)',
        }
    }
    if (level === 'crit') {
        return {
            label: 'КРИТ',
            color: 'rgb(255,0,0)',
            background: 'rgba(1, 1, 1, 1)',
        }
    }
}


export const IncidentLevel = ({ level }) => {
    const colors = get_level(level)

    return <div style={{
        userSelect: 'none',
        textAlign: "center",
        padding: '3px 10px',
        color: colors.color,
        borderColor: colors.color,
        backgroundColor: colors.background,
        fontWeight: 'bolder',
    }} className='rounded_border'>
        {colors.label}
    </div>
}

export default IncidentLevel;