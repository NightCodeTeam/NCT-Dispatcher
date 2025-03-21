import aiosqlite
from ..debug import create_log
from ..single import Singleton


class SQLiteDB(Singleton):
    db_name: str

    def __init__(self, db_location: str):
        self.db_name = db_location

    async def _execute(self, query: str, commit: bool = True) -> bool:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute(query)
                if commit:
                    await db.commit()
                return True
        except aiosqlite.Error as err:
            create_log(err, 'error')
            return False

    async def _fetchall(self, query, commit: bool = False) -> tuple:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                async with db.execute(query) as cursor:
                    if commit:
                        await db.commit()
                    return tuple(await cursor.fetchall())
        except aiosqlite.Error as err:
            create_log(err, 'error')
            return ()

    async def _commit(self) -> bool:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.commit()
            return True
        except aiosqlite.Error as err:
            create_log(err, 'error')
            return False
