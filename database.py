import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            key TEXT UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            approved BOOLEAN DEFAULT FALSE
        )''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def create_post(self, message, key):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO posts (message, key) VALUES (?, ?)", (message, key))
        self.conn.commit()

    def get_post(self, key):
        cursor = self.conn.cursor()
        post = cursor.execute("SELECT * FROM posts WHERE key = ?", (key,)).fetchone()
        return post

    def update_post(self, key, message):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE posts SET message = ? WHERE key = ?", (message, key))
        self.conn.commit()

    def delete_post(self, key):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM posts WHERE key = ?", (key,))
        self.conn.commit()
