import api from './main.jsx'


export const apps_service = {
    all_apps: async (skip=0, limit=0) => {
        return (await api.get('/v1/apps/', {
            params: {
                skip: skip,
                limit: limit,
            }
        })).data.apps || []
    },

    app_detail: async (app_id) => {
        return (await api.get(`/v1/apps/${app_id}`)).data
    },

    app_logs: async (app_id) => {
        return (await api.get(`/v1/apps/${app_id}/logs`)).data.logs || []
    },

    new_app: async (name, status_url, logs_folder) => {
        return (await api.post('/v1/apps/new', {
            name: name,
            status_url: status_url,
            logs_folder: logs_folder,
        })).data.ok || false
    },

    del_app: async (app_id) => {
        return (await api.delete(`/v1/apps/${app_id}`)).data.ok || false
    },
};

export default apps_service;