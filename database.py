import sqlite3

class Database():
    def __init__(self,db_file):
        self.connection=sqlite3.connect(db_file,check_same_thread=False)
        self.cursor= self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(signup VARCHAR DEFAULT setnickname, user_id INTEGER, nickname VARCHAR)""")



    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute("""INSERT INTO users (user_id) VALUES (?)""",(user_id,))

    def user_exists(self, user_id):
        with self.connection:
            self.result = self.cursor.execute("""SELECT * FROM users WHERE user_id = ?""",(user_id,)).fetchall()
            return bool(self.result)

    def set_nickname (self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("""UPDATE users SET nickname = ? WHERE user_id = ? """,(nickname, user_id))

    def get_signup(self, user_id):
        with self.connection:
            return self.cursor.execute("""SELECT signup FROM users WHERE user_id = ?""",(user_id,)).fetchall()

    def set_signup (self, user_id, signup):
        with self.connection:
            return self.cursor.execute("""UPDATE users SET signup = ? WHERE user_id = ? """,(signup, user_id))
