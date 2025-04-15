import requests
from .dispatcher_settings import Level


def post_incident(
    dispatcher_url: str,
    dispatcher_code: str,
    app_name: str,

    title: str,
    message: str,
    level: Level,
    logs: str | list[str] | tuple[str] | None = None,
) -> bool:
    if type(logs) is list or type(logs) is tuple:
        logs='\n'.join(logs)
    res = requests.post(
        url=dispatcher_url,
        json={
            'title': title,
            'message': message,
            'level': level,
            'logs': logs,
            'app_name': app_name,
        }, headers={
            'Content-Type': 'application/json',
            'dispatch': dispatcher_code,
        }
    )
    return True if res is not None and res.json()['ok'] == True else False