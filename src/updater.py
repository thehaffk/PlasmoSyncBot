import sqlite3
from settings import config

conn = sqlite3.connect(config['db'])
cursor = conn.cursor()

def fix_db():
    row = cursor.execute('SELECT * FROM servers WHERE guild_id = 828683007635488809').fetchone()
    if len(row) < 13:
        print('Wrond DB')
    else:
        print('Database already fixed')