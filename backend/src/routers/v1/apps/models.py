from typing import List
from pydantic import BaseModel


class NewAppRequest(BaseModel):
    """
    Создание нового приложения:
        - name: название приложения
        - status_url: URL для проверки статуса приложения
        - status_code: код статуса, который должен быть возвращен для успешной проверки
        - logs_folder: папка для хранения логов
        - script_path: путь к скрипту приложения
    """
    name: str
    status_url: str
    status_code: str | None = None
    logs_folder: str | None = None
    script_path: str | None = None


class AppUpdateRequest(BaseModel):
    """
    Модель для обновления информации об приложении.
        - name: название приложения
        - status_url: URL для проверки статуса приложения
        - status_code: код статуса, который должен быть возвращен для успешной проверки
        - logs_folder: папка для хранения логов
        - script_path: путь к скрипту приложения
        - new_code: флаг, указывающий на необходимость обновления кода приложения
    """
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
    """
    Модель для ответа с информацией об приложении.
    """
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
	"""
	Модель для ответа с файлом лога приложения.
	title - заголовок файла лога
	log - содержимое файла с логами
	"""
	title: str
	log: str


class AppMultipleLogFilesResponse(BaseModel):
    """
    Модель для ответа с несколькими файлами логов приложения.
    """
    logs: List[AppLogFileResponse]


class MultipleAppsResponse(BaseModel):
    """
    Модель для ответа с несколькими приложениями.
    """
    apps: List[AppResponse]
