import api from './main.jsx'


export const incidents_service = {
    all_incidents: async (skip_= 0, limit_= 10) => {
        return (await api.get(`v1/incidents/`, {
            params: {
                skip: skip_,
                limit: limit_,
            }
        })).data.incidents || []
    },

    incident_detail: async (incident_id) => {
        return (await api.get(`/v1/incidents/${incident_id}`)).data
    },

    new_incident: async (name, status_url, logs_folder) => {
        return (await api.post('/v1/incidents/new', {
            name: name,
            status_url: status_url,
            logs_folder: logs_folder,
        })).data.ok || false
    },

    del_incident: async (incident_id) => {
        return (await api.delete(`/v1/incidents/${incident_id}`)).data.ok || false
    },

    update_incident: async (incident_id, new_status) => {
        return (await api.put(`/v1/incidents/${incident_id}/status`, {
            new_status: new_status,
        })).data.ok || false
    }
};

export default incidents_service;