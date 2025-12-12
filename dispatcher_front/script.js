document.addEventListener('DOMContentLoaded', function() {
    // Элементы DOM
    const mainContent = document.getElementById('main-content');
    const navLinks = document.getElementById('nav-links');
    const logoutBtn = document.getElementById('logout-btn');
    const appModal = document.getElementById('app-modal');
    const closeModalBtn = document.querySelector('.close-modal');
    const appForm = document.getElementById('app-form');

    // Проверка авторизации и загрузка страницы
    checkAuth();

    // Обработчики событий навигации
    navLinks.addEventListener('click', function(e) {
        e.preventDefault();

        if (e.target.tagName === 'A') {
            const page = e.target.getAttribute('data-page');
            loadPage(page);
        }
    });

    // Выход из системы
    logoutBtn.addEventListener('click', function() {
        logout();
    });

    // Закрытие модального окна
    closeModalBtn.addEventListener('click', function() {
        appModal.style.display = 'none';
    });

    // Закрытие модального окна при клике вне его
    window.addEventListener('click', function(e) {
        if (e.target === appModal) {
            appModal.style.display = 'none';
        }
    });

    // Создание нового приложения
    appForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const appName = document.getElementById('app-name').value;
        const appDescription = document.getElementById('app-description').value;
        const appOwner = document.getElementById('app-owner').value;

        if (appName && appOwner) {
            createApplication(appName, appDescription, appOwner);
            appModal.style.display = 'none';
            appForm.reset();
        }
    });

    // Функция проверки авторизации
    function checkAuth() {
        const isLoggedIn = api.isAuthenticated();

        if (!isLoggedIn) {
            loadLoginPage();
        } else {
            loadPage('incidents');
        }
    }

    // Функция загрузки страницы
    function loadPage(page) {
        if (!api.isAuthenticated()) {
            loadLoginPage();
            return;
        }

        switch(page) {
            case 'incidents':
                loadIncidentsPage();
                break;
            case 'applications':
                loadApplicationsPage();
                break;
            default:
                loadIncidentsPage();
        }
    }

    // Страница логина
    function loadLoginPage() {
        const loginHTML = `
            <div class="login-container">
                <h2><i class="fas fa-sign-in-alt"></i> Вход в систему</h2>
                <form id="login-form">
                    <div class="form-group">
                        <label for="username">Имя пользователя:</label>
                        <input type="text" id="username" value="admin" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Пароль:</label>
                        <input type="password" id="password" value="password" required>
                    </div>
                    <button type="submit" class="btn btn-primary" style="width:100%;">Войти</button>
                </form>
                <div style="margin-top:1rem; text-align:center; color:#666;">
                    <p>Используйте admin / password для входа</p>
                </div>
            </div>
        `;

        mainContent.innerHTML = loginHTML;

        // Скрываем навигацию
        document.getElementById('navbar').style.display = 'none';

        // Обработчик формы входа
        document.getElementById('login-form').addEventListener('submit', function(e) {
            e.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (api.login(username, password)) {
                document.getElementById('navbar').style.display = 'block';
                loadPage('incidents');
            } else {
                alert('Неверное имя пользователя или пароль!');
            }
        });
    }

    // Страница инцидентов
    function loadIncidentsPage() {
        const incidents = api.getIncidents();

        let incidentsHTML = '';
        incidents.forEach(incident => {
            const logsHTML = incident.logs.map(log =>
                `<div class="log-entry">${log.timestamp} - ${log.message}</div>`
            ).join('');

            incidentsHTML += `
                <tr>
                    <td>${incident.id}</td>
                    <td>
                        <strong>${incident.title}</strong>
                        <div class="logs-container">${logsHTML}</div>
                    </td>
                    <td>${incident.description}</td>
                    <td>${incident.application}</td>
                    <td>
                        <span class="status-badge status-${incident.status}">
                            ${incident.status === 'open' ? 'Открыт' : 'Закрыт'}
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-${incident.status === 'open' ? 'success' : 'warning'} toggle-status" data-id="${incident.id}">
                            ${incident.status === 'open' ? 'Закрыть' : 'Открыть'}
                        </button>
                    </td>
                </tr>
            `;
        });

        const pageHTML = `
            <div class="page">
                <div class="page-header">
                    <h2><i class="fas fa-exclamation-triangle"></i> Управление инцидентами</h2>
                    <div>
                        <button class="btn btn-primary" id="refresh-incidents">
                            <i class="fas fa-sync-alt"></i> Обновить
                        </button>
                    </div>
                </div>

                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Название / Логи</th>
                                <th>Описание</th>
                                <th>Приложение</th>
                                <th>Статус</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${incidentsHTML}
                        </tbody>
                    </table>
                </div>

                <div style="margin-top: 2rem; text-align: center; color: #666;">
                    <p>Всего инцидентов: ${incidents.length} | Открыто: ${incidents.filter(i => i.status === 'open').length}</p>
                </div>
            </div>
        `;

        mainContent.innerHTML = pageHTML;

        // Обработчики событий для кнопок изменения статуса
        document.querySelectorAll('.toggle-status').forEach(button => {
            button.addEventListener('click', function() {
                const incidentId = parseInt(this.getAttribute('data-id'));
                toggleIncidentStatus(incidentId);
            });
        });

        // Обновление списка инцидентов
        document.getElementById('refresh-incidents').addEventListener('click', function() {
            loadIncidentsPage();
        });
    }

    // Страница приложений
    function loadApplicationsPage() {
        const applications = api.getApplications();

        let applicationsHTML = '';
        applications.forEach(app => {
            applicationsHTML += `
                <tr>
                    <td>${app.id}</td>
                    <td><strong>${app.name}</strong></td>
                    <td>${app.description}</td>
                    <td>${app.owner}</td>
                    <td>${app.incidentCount}</td>
                    <td>
                        <span class="status-badge ${app.status === 'active' ? 'status-closed' : 'status-open'}">
                            ${app.status === 'active' ? 'Активно' : 'Неактивно'}
                        </span>
                    </td>
                </tr>
            `;
        });

        const pageHTML = `
            <div class="page">
                <div class="page-header">
                    <h2><i class="fas fa-server"></i> Управление приложениями</h2>
                    <div>
                        <button class="btn btn-primary" id="create-app-btn">
                            <i class="fas fa-plus"></i> Создать приложение
                        </button>
                    </div>
                </div>

                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Название</th>
                                <th>Описание</th>
                                <th>Владелец</th>
                                <th>Инцидентов</th>
                                <th>Статус</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${applicationsHTML}
                        </tbody>
                    </table>
                </div>

                <div style="margin-top: 2rem; text-align: center; color: #666;">
                    <p>Всего приложений: ${applications.length}</p>
                </div>
            </div>
        `;

        mainContent.innerHTML = pageHTML;

        // Открытие модального окна для создания приложения
        document.getElementById('create-app-btn').addEventListener('click', function() {
            appModal.style.display = 'flex';
        });
    }

    // Изменение статуса инцидента
    function toggleIncidentStatus(id) {
        api.toggleIncidentStatus(id);
        loadIncidentsPage();
    }

    // Создание нового приложения
    function createApplication(name, description, owner) {
        api.createApplication(name, description, owner);
        loadApplicationsPage();
    }

    // Выход из системы
    function logout() {
        api.logout();
        checkAuth();
    }
});
