// Мок API для демонстрации работы фронтенда
const api = {
    // Текущий пользователь
    currentUser: null,

    // Данные приложений
    applications: [
        { id: 1, name: 'Веб-портал', description: 'Основной веб-портал компании', owner: 'Иван Петров', incidentCount: 3, status: 'active' },
        { id: 2, name: 'Мобильное приложение', description: 'Приложение для iOS и Android', owner: 'Мария Сидорова', incidentCount: 1, status: 'active' },
        { id: 3, name: 'API сервис', description: 'Основное API для интеграций', owner: 'Алексей Иванов', incidentCount: 2, status: 'inactive' },
        { id: 4, name: 'База данных', description: 'Основная база данных клиентов', owner: 'Ольга Николаева', incidentCount: 0, status: 'active' }
    ],

    // Данные инцидентов
    incidents: [
        {
            id: 1,
            title: 'Ошибка авторизации',
            description: 'Пользователи не могут войти в систему через социальные сети',
            application: 'Веб-портал',
            status: 'open',
            logs: [
                { timestamp: '2023-10-05 09:15:23', message: 'Обнаружена ошибка в модуле авторизации' },
                { timestamp: '2023-10-05 09:30:45', message: 'Начато исследование проблемы' },
                { timestamp: '2023-10-05 10:15:12', message: 'Обнаружена проблема с API социальных сетей' }
            ]
        },
        {
            id: 2,
            title: 'Медленная загрузка страниц',
            description: 'Страницы загружаются более 5 секунд',
            application: 'Мобильное приложение',
            status: 'closed',
            logs: [
                { timestamp: '2023-10-04 14:20:11', message: 'Пользователи сообщают о медленной загрузке' },
                { timestamp: '2023-10-04 15:05:33', message: 'Проблема локализована в кэшировании изображений' },
                { timestamp: '2023-10-04 16:30:09', message: 'Применено исправление, проблема решена' }
            ]
        },
        {
            id: 3,
            title: 'Ошибка 500 на API',
            description: 'Некоторые эндпоинты возвращают ошибку сервера',
            application: 'API сервис',
            status: 'open',
            logs: [
                { timestamp: '2023-10-05 11:45:30', message: 'Получены сообщения об ошибках 500' },
                { timestamp: '2023-10-05 12:15:22', message: 'Обнаружена проблема с подключением к базе данных' }
            ]
        },
        {
            id: 4,
            title: 'Неверное отображение данных',
            description: 'В отчетах отображаются некорректные цифры',
            application: 'Веб-портал',
            status: 'open',
            logs: [
                { timestamp: '2023-10-03 16:10:05', message: 'Финансовый отдел сообщил о неверных данных в отчетах' }
            ]
        },
        {
            id: 5,
            title: 'Падение сервера',
            description: 'Сервер был недоступен в течение 10 минут',
            application: 'API сервис',
            status: 'closed',
            logs: [
                { timestamp: '2023-10-02 03:15:00', message: 'Сервер перестал отвечать на запросы' },
                { timestamp: '2023-10-02 03:20:45', message: 'Запущена процедура перезагрузки' },
                { timestamp: '2023-10-02 03:25:30', message: 'Сервер восстановлен, причина - перегрузка памяти' }
            ]
        }
    ],

    // Проверка авторизации
    isAuthenticated: function() {
        return this.currentUser !== null;
    },

    // Вход в систему
    login: function(username, password) {
        // В демо-версии принимаем любые непустые учетные данные
        if (username && password) {
            this.currentUser = {
                username: username,
                name: 'Администратор'
            };

            // Сохраняем в localStorage для сохранения сессии
            localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
            return true;
        }

        return false;
    },

    // Выход из системы
    logout: function() {
        this.currentUser = null;
        localStorage.removeItem('currentUser');
    },

    // Получение списка инцидентов
    getIncidents: function() {
        return this.incidents;
    },

    // Изменение статуса инцидента
    toggleIncidentStatus: function(id) {
        const incident = this.incidents.find(i => i.id === id);
        if (incident) {
            incident.status = incident.status === 'open' ? 'closed' : 'open';

            // Добавляем запись в логи
            const timestamp = new Date().toISOString().replace('T', ' ').substr(0, 19);
            const message = incident.status === 'closed' ? 'Инцидент закрыт пользователем' : 'Инцидент вновь открыт пользователем';
            incident.logs.push({ timestamp, message });
        }
    },

    // Получение списка приложений
    getApplications: function() {
        // Обновляем количество инцидентов для каждого приложения
        this.applications.forEach(app => {
            app.incidentCount = this.incidents.filter(incident => incident.application === app.name).length;
        });

        return this.applications;
    },

    // Создание нового приложения
    createApplication: function(name, description, owner) {
        const newId = this.applications.length > 0
            ? Math.max(...this.applications.map(app => app.id)) + 1
            : 1;

        const newApp = {
            id: newId,
            name: name,
            description: description,
            owner: owner,
            incidentCount: 0,
            status: 'active'
        };

        this.applications.push(newApp);
        return newApp;
    }
};

// Восстановление сессии при загрузке страницы
window.addEventListener('load', function() {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        api.currentUser = JSON.parse(savedUser);
    }
});
