import sqlite3
from settings import config

conn = sqlite3.connect(config['db'])
cursor = conn.cursor()

def fix_db():
    row = cursor.execute('SELECT * FROM servers WHERE guild_id = 828683007635488809').fetchone()
    if len(row) < 13:
        print('Fixing database...')
        cursor.execute('''PRAGMA foreign_keys = 0;

    CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                              FROM servers;
    
    DROP TABLE servers;
    
    CREATE TABLE servers (
        guild_id        INT     NOT NULL
                                UNIQUE,
        on_join         BOOLEAN NOT NULL
                                DEFAULT False,
        everyone        BOOLEAN NOT NULL
                                DEFAULT False,
        server          STRING  NOT NULL
                                DEFAULT RP,
        sync_roles      BOOLEAN NOT NULL
                                DEFAULT False,
        sync_nick       BOOLEAN NOT NULL
                                DEFAULT True,
        player_role     INTEGER,
        fusion_role     INTEGER,
        helper_role     INTEGER,
        banker_role     INTEGER,
        mko_head_role   INTEGER,
        mko_helper_role INTEGER,
        mko_member_role INTEGER
    );
    
    INSERT INTO servers (
                            guild_id,
                            on_join,
                            everyone,
                            server,
                            sync_roles,
                            sync_nick,
                            player_role,
                            fusion_role,
                            helper_role
                        )
                        SELECT guild_id,
                               on_join,
                               everyone,
                               server,
                               sync_roles,
                               sync_nick,
                               player_role,
                               fusion_role,
                               helper_role
                          FROM sqlitestudio_temp_table;
    
    DROP TABLE sqlitestudio_temp_table;
    
    PRAGMA foreign_keys = 1;
        ''')
        conn.commit()
        print('Database fixed')
    else:
        print('Database already fixed')