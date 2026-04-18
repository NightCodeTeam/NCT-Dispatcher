from src.database import DataBase, Incident
from src.services import auth_service
from core.redis_client import RedisClient


class IncidentsHandler:
    def __init__(self, db: DataBase):
        self.db = db

    async def all(
        self,
        redis: RedisClient,
        skip: int | None = 0,
        limit: int | None = 100,
    ) -> list[dict]:
        """
        Получает список всех инцидентов.
        """
        incidents = await self.db.incidents.pagination(
            skip=skip or 0,
            limit=limit or 100,
            load_relations=True,
        )
        return [{
            'id': i.id,
            'title': i.title,
            'message': i.message,
            'logs': i.logs,
            'level': i.level,
            'status': i.status,
            'app_name': i.app.name,
            'created_at': i.created_at.isoformat(),
            'updated_at': i.updated_at.isoformat(),
            'edit_by_user': await auth_service.user_by_id(
                i.edit_by_id, redis
            ) if i.edit_by_id else None
        } for i in incidents]

    async def by_id(self, incident: Incident, redis: RedisClient) -> dict | None:
        """
        Получает инцидент по ID.
        """
        return {
            'id': incident.id,
            'title': incident.title,
            'message': incident.message,
            'logs': incident.logs,
            'level': incident.level,
            'status': incident.status,
            'app_name': incident.app.name,
            'created_at': incident.created_at.isoformat(),
            'updated_at': incident.updated_at.isoformat(),
            'edit_by_user': await auth_service.user_by_id(
                incident.edit_by_id, redis
            ) if incident.edit_by_id else None
        }
