import json
from database.models import Incident, App
from database.utils import get_apps_from_db, get_incidents_from_db

from .bot_settings import BotCallbacks


async def incident_markup(incident_id: int) -> dict:
    return {
        'reply_markup': json.dumps({
            'inline_keyboard': [
                {'text': 'Закрыть', 'callback_data': f'{BotCallbacks.CLOSE_INCIDENT}{incident_id}'},
                #{'text': 'Edit', 'callback_data': f'edit_incident_{incident_id}'},
                {'text': 'Удалить', 'callback_data': f'{BotCallbacks.DEL_INCIDENT}{incident_id}'}
            ]
        })
    }


async def new_app_markup() -> dict:
    return {
        'reply_markup': json.dumps({
            'inline_keyboard': [
                {'text': 'Название', 'switch_inline_query_current_chat': f'{BotCallbacks.NEW_APP}_name'},
                {'text': 'url', 'switch_inline_query_current_chat': f'{BotCallbacks.NEW_APP}_back_url'},
                {'text': 'Создать', 'callback_data': f'{BotCallbacks.NEW_APP}_create'}
            ]
        })
    }


async def select_app_markup() -> dict:
    apps = await get_apps_from_db()
    ans = []
    for app in apps:
        ans.append([
            {'text': app.name, 'callback_data': f'{BotCallbacks.SELECT_APP}{app.id}'}
        ])
    return {
        'reply_markup': json.dumps({
            'inline_keyboard': ans
        })
    }


async def app_incidents_markup(app_id: int) -> dict:
    incidents = await get_incidents_from_db(filter=f'apps={app_id}')
    ans = []
    for incident in incidents:
        ans.append([
            {'text': incident.title, 'callback_data': f'{BotCallbacks.SELECT_INCIDENT}{incident.id}'}
        ])
    return {
        'reply_markup': json.dumps({
            'inline_keyboard': ans
        })
    }
