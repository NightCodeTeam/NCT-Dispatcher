export const AppChange = ({handleChange, form_submit, formData}) => {
    return <form className='base_flex_column' onSubmit={(e) => form_submit(e)} style={{
        width: '100%',
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
        />
        <input
            type='text'
            name='status_url'
            style={{padding: 5, width: '100%'}}
            className='rounded_border'
            placeholder='Статус URL'
            value={formData.status_url}
            onChange={handleChange}
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
        <label className='base_flex_row' style={{width:'100%'}}>
            <input
                type='checkbox'
                name='new_code'
                className='rounded_border'
                placeholder='Сгенерировать новый код'
                value={formData.new_code}
                onChange={handleChange}
            />
            Новый код?
        </label>
        <input type='submit' style={{padding: 5}} className='rounded_border' value='Изменить'/>
    </form>
}