from typing import List
from pydantic import BaseModel


class NewAppRequest(BaseModel):
    name: str
    status_url: str | None = None
    logs_folder: str | None = None


class IncidentResponse(BaseModel):
    title: str
    msg: str
    level: str
    logs: str


class AppResponse(BaseModel):
    name: str
    status_url: str
    incidents: List[IncidentResponse]


class AppLogFileResponse(BaseModel):
    title: str
    log: str


class AppMultipleLogFilesResponse(BaseModel):
    logs: List[AppLogFileResponse]


class MultipleAppsResponse(BaseModel):
    apps: List[AppResponse]
