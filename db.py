import os
import sqlite3

DB_FILENAME = 'downloads.db'


# def connect() -> sqlite3.Connection:
#     conn = sqlite3.connect(DB_FILENAME)
#     return conn


def persist_download(title, season, episode):
    conn = sqlite3.connect(DB_FILENAME)
    identifier = "{}S{}E{}".format(title, str(season), str(episode))
    sql = "INSERT INTO download(identifier, title, season, episode) VALUES ('{}', '{}', '{}', '{}')".format(identifier,
                                                                                                            title,
                                                                                                            season,
                                                                                                            episode)
    conn.execute(sql)
    conn.commit()
    conn.close()


def download_exists(title: str, season: int, episode: int):
    identifier = "{}S{}E{}".format(title, str(season), str(episode))
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    sql = "select * from download where identifier = '{}'".format(identifier)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(result) > 0:
        return True
    return False
