from typing import List
from pydantic import BaseModel


class NewAppRequest(BaseModel):
	name: str
	status_url: str
	status_code: str | None = None
	logs_folder: str | None = None
	script_path: str | None = None


class AppUpdateRequest(BaseModel):
    name: str | None = None
    status_url: str | None = None
    status_code: str | None = None
    logs_folder: str | None = None
    script_path: str | None = None
    new_code: bool | None = None


class IncidentResponse(BaseModel):
	title: str
	message: str
	level: str
	logs: str


class AppStatusResponse(BaseModel):
	ok: bool = False
	cpu_usage: float | int = 0
	memory_usage: float | int = 0
	disk_usage: float | int = 0
	adt_data: dict | None = None


class AppResponse(BaseModel):
	id: int
	name: str
	code: str
	status: AppStatusResponse
	status_url: str
	status_code: str | None = None
	logs_folder: str | None = None
	script_path: str | None = None
	incidents_count: int


class AppLogFileResponse(BaseModel):
	title: str
	log: str


class AppMultipleLogFilesResponse(BaseModel):
	logs: List[AppLogFileResponse]


class MultipleAppsResponse(BaseModel):
	apps: List[AppResponse]
