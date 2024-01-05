import sqlite3

CONN = sqlite3.connect('music.db')
CURSOR = CONN.cursor()


class Song:
    # keep track of objects/list of objects
    all = []

    def __init__(self, name, album):
        self.id = None
        self.name = name
        self.album = album

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS songs
        """

        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO songs (name, album)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.album))

        # always update id after inserting
        self.id = CURSOR.execute(
            "SELECT last_insert_rowid() FROM songs").fetchone()[0]
        # OR
        # self.id = CURSOR.lastrowid

    # DRY/prevent creating instance/object every time
    @classmethod
    def create(cls, name, album):
        song = Song(name, album)
        song.save()
        return song

    # new code goes here!
    @classmethod
    def new_from_db(cls, row):
        # access class constructor through cls/create new python object
        song = cls(row[1], row[2])
        song.id = row[0]
        
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM songs
        """
        # fetch all rows from last executed statement
        all = CURSOR.execute(sql).fetchall()

        # update all with new python objects/list(array) of objects
        cls.all = [cls.new_from_db(row) for row in all]
        
    @classmethod
    def find_by_name(cls, name):
        # use ? placeholder to prevent sql injections
        sql = """
            SELECT *
            FROM songs
            WHERE name = ?
            LIMIT 1
        """

        song = CURSOR.execute(sql, (name,)).fetchone()

        # return python object
        return cls.new_from_db(song)
        
    
