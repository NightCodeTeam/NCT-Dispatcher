import api from "@/api/base.jsx";

export const back_service = {
    apps: {
        all: async ({skip = 0, limit = 10}) => {
            return (await api.get('/v1/apps', {
                params: {
                    skip: skip,
                    limit: limit,
                }
            })).data.apps || []
        },

        detail: async (app_id) => {
            return (await api.get(`/v1/apps/${app_id}`)).data
        },

        logs: async (app_id) => {
            return (await api.get(`/v1/apps/${app_id}/logs`)).data.logs || []
        },

        new: async ({name, status_url, status_code, logs_folder, script}) => {
            return (await api.post('/v1/apps/new', {
                name: name,
                status_url: status_url,
                status_code: status_code,
                logs_folder: logs_folder,
                script: script
            })).data.ok || false
        },

        update: async ({app_id, name, status_url, status_code, logs_folder, script_path, new_code}) => {
            return (await api.put(`/v1/apps/${app_id}`, {
                name: name,
                status_url: status_url,
                status_code: status_code,
                logs_folder: logs_folder,
                script_path: script_path,
                new_code: new_code,
            }))?.data.ok || false
        },

        del: async (app_id) => {
            return (await api.delete(`/v1/apps/${app_id}`)).data.ok || false
        },
    },
    incidents: {
        all: async ({skip_ = 0, limit_ = 10}) => {
            return (await api.get(`v1/incidents`, {
                params: {
                    skip: skip_,
                    limit: limit_,
                }
            })).data.incidents.sort((a, b) => b.created_at.localeCompare(a.created_at)) || []
        },

        detail: async (incident_id) => {
            return (await api.get(`/v1/incidents/${incident_id}`)).data
        },

        del: async (incident_id) => {
            return (await api.delete(`/v1/incidents/${incident_id}`)).data.ok || false
        },

        update: async ({incident_id, new_status}) => {
            return (await api.put(`/v1/incidents/${incident_id}/status`, {
                new_status: new_status,
            })).data.ok || false
        }
    }
}

export default back_service;