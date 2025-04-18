from typing import Final


BOT_MAX_UPDATES: Final = 100
BOT_PREFIX: Final = '/'
BOT_SLEEP_TIME_IN_SEC: Final = 1

class BotCommands:
    HELP = "help"
    START = "start"
    NEW_APP = "new"


class BotCallbacks:
    BACK = "back"

    ALL_INCIDENTS = "all_incidents"
    OPEN_INCIDENTS = "open_incidents"
    SELECT_INCIDENT = "select_incident_"
    CLOSE_INCIDENT = "close_incident_"
    DEL_INCIDENT = "del_incident_"

    ALL_APPS = "all_apps"
    NEW_APP = "new_app"
    NEW_APP_NAME = "new_app_name"
    NEW_APP_URL = "new_app_url"
    NEW_APP_CONFIRM = "new_app_confirm"
    NEW_APP_CANCEL = "new_app_cancel"
    SELECT_APP = "app_"
    SELECT_APP_INCIDENTS = 'app_incedents_'
    DEL_APP = "del_app_"

    ALL_BANS = "bans"
    SELECT_BAN = "ban_"
    DELETE_BAN = "del_ban_"
