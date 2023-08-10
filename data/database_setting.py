import aiosqlite
import sqlite3
import datetime
class DataBase:
    def __init__(self, database_name):
        self.db_name = database_name
    
    # Работа с БД
    async def create_tables(self) -> None: # Создание таблиц
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('CREATE TABLE IF NOT EXISTS sponsors (channel_id INTEGER, channel_link VARCHAR(200))')
            await db.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, is_admin INTEGER DEFAULT 0, first_name VARCHAR(200), ref VARCHAR(255))')
            await db.execute('CREATE TABLE IF NOT EXISTS ref (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(120), referals INTEGER DEFAULT 0)')
            await db.commit()
        
        await self.new_columns()
    
    async def new_columns(self):
        await self.__new_columns('users', 'ref', 'VARCHAR(255)')

    async def __new_columns(self, table_name, column_name, type_column) -> None:
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {type_column}')
                await db.commit()
        except sqlite3.OperationalError:
            pass
    
    # Работа с юзерами
    async def create_user(self, tg_id: int, first_name: str):
        import datetime
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('INSERT INTO users (user_id, first_name, click) VALUES (?, ?, ?)', (tg_id, first_name, datetime.datetime.now() - datetime.timedelta(minutes=10)))
            await db.commit()
    
    async def get_user(self, tg_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM users WHERE user_id = ?', (tg_id, )) as cursor:
                return await cursor.fetchone()
            
    async def get_all_users(self):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM users') as cursor:
                return await cursor.fetchall()

    async def get_all_active_users(self) -> list:
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM users WHERE click > ?', (datetime.date.today() - datetime.timedelta(hours=24),)) as cursor:
                return await cursor.fetchall()
    
    async def get_all_admins(self):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM users WHERE is_admin = 1') as cursor:
                return await cursor.fetchall()
            
    async def add_admin(self, tg_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET is_admin = 1 WHERE user_id = ?', (tg_id,))
            await db.commit()
    
    async def delete_admin(self, tg_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET is_admin = 0 WHERE user_id = ?', (tg_id,))
            await db.commit()
    
    async def add_user_ref(self, tg_id: int, ref:str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET ref = ? WHERE user_id = ?', (ref, tg_id))
            await db.commit()

    async def delete_user_ref(self, tg_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE users SET ref = "" WHERE user_id = ?', (tg_id,))
            await db.commit()
    
    async def get_all_user_ref(self, ref:str):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM users WHERE ref = ?', (ref,)) as cursor:
                return await cursor.fetchall()

    # Работа со спонсорами
    async def create_sponsor(self, channel_id: int, channel_link: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('INSERT INTO sponsors (channel_id, channel_link) VALUES (?, ?)', (channel_id, channel_link))
            await db.commit()
    
    async def get_all_sponsors(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM sponsors') as cursor:
                return await cursor.fetchall()
            
    async def get_sponsor(self, sponsor_id):
        async with aiosqlite.connect(self.db_name) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('SELECT * FROM sponsors WHERE channel_id = ?', (sponsor_id, )) as cursor:
                return await cursor.fetchone()
    
    async def delete_sponsor(self, chat_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM sponsors WHERE channel_id = ?', (chat_id, ))
            await db.commit()
    
    # Работа с рефералами
    async def create_ref(self, name: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('INSERT INTO ref (name) VALUES (?)', (name, ))
            await db.commit()

    async def delete_ref(self, name: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('DELETE FROM ref WHERE name = ?', (name, ))
            await db.commit()

    async def change_ref(self, name: str, new_name: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE ref SET name = ? WHERE name = ?', (new_name, name))
            await db.commit()
    
    async def get_ref(self, name: str):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM ref WHERE name = ?', (name, )) as cursor:
                res = await cursor.fetchone()
        
            if res:
                return {
                    'id': res[0],
                    'name': res[1],
                    'referals': res[2]
                }
        return {}
    
    async def get_all_ref(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM ref ORDER BY referals DESC') as cursor:
                return await cursor.fetchall()

    async def add_ref(self, name: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE ref SET referals = referals + 1 WHERE name = ?', (name,))
            await db.commit()
    

db = DataBase('Kreash_Kid.sqlite')