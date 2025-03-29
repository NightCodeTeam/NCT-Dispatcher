from typing import Final


BOT_MAX_UPDATES: Final = 100
BOT_PREFIX: Final = '/'
BOT_SLEEP_TIME_IN_SEC: Final = 1

class BotCommands:
    HELP = "help"
    START = "start"


class BotCallbacks:
    SELECT_INCIDENT = "select_incident_"
    CLOSE_INCIDENT = "close_incident_"
    DEL_INCIDENT = "del_incident_"

    ALL_APPS = "all_apps"
    NEW_APP = "new_app"
    SELECT_APP = "app_"
