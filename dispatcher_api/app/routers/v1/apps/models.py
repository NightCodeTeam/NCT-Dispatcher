from typing import List
from pydantic import BaseModel


class NewAppRequest(BaseModel):
	name: str
	status_url: str | None = None
	logs_folder: str | None = None


class IncidentResponse(BaseModel):
	title: str
	message: str
	level: str
	logs: str


class AppResponse(BaseModel):
	id: int
	name: str
	code: str
	status_url: str
	logs_folder: str | None = None
	incidents: list[str]


class AppLogFileResponse(BaseModel):
	title: str
	log: str


class AppMultipleLogFilesResponse(BaseModel):
	logs: List[AppLogFileResponse]


class MultipleAppsResponse(BaseModel):
	apps: List[AppResponse]
