export const NewAppForm = ({ handleChange, form_submit, formData}) => {
    return <form className='base_flex_column' onSubmit={() => form_submit()} style={{
        width: '100%',
        padding: '5px',
        alignItems: 'flex-start',
    }}>
        <input
            type='text'
            name='name'
            style={{padding: 5, width: '100%'}}
            className='rounded_border'
            placeholder='Название'
            value={formData.name}
            onChange={handleChange}
            required
        />
        <input
            type='text'
            name='status_url'
            style={{padding: 5, width: '100%'}}
            className='rounded_border'
            placeholder='Статус URL'
            value={formData.status_url}
            onChange={handleChange}
            required
        />
        <input
            type='text'
            name='status_code'
            style={{padding: 5, width: '100%'}}
            className='rounded_border'
            placeholder='Код доступа'
            value={formData.status_code}
            onChange={handleChange}
        />
        <input
            type='text'
            name='logs_folder'
            style={{padding: 5, width: '100%'}}
            className='rounded_border'
            placeholder='Папка логов (полный путь)'
            value={formData.logs_folder}
            onChange={handleChange}
        />
        <input
            type='text'
            name='script'
            style={{padding: 5, width: '100%'}}
            className='rounded_border'
            placeholder='Скрипт запуска (полный путь)'
            value={formData.script}
            onChange={handleChange}
        />
        <input type='submit' style={{padding: 5}} className='rounded_border' value='Создать'/>
    </form>
}

export default NewAppForm;