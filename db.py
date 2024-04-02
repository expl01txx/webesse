import sqlite3

class DataBase:
    def __init__(self):
        self.db = sqlite3.connect("db/webesse.db")
    def auth(self, login: str, passwd: str) -> bool:
        result = self.db.execute("SELECT * FROM users WHERE login = ? AND passwd = ?", (login, passwd))
        if result.fetchone():
            return True
        else:
            return False

    
    def add_user(self, login: str, passwd: str):
        self.db.execute("INSERT INTO users (login, passwd, tokens, admin, esse_checks) VALUES (?, ?, ?, ?, ?)", (login, passwd, 10, 0, 0))
        self.db.commit()

    def add_usage(self, login: str):
        self.db.execute("UPDATE users SET tokens = tokens - 1, esse_checks = esse_checks + 1, last_activity = datetime('now') WHERE login = ?", (login,))
        self.db.commit()
    
    def add_log(self, login: str, esse_task: str, esse_content: str, esse_result: str):
        self.db.execute("INSERT INTO logs (login, esse_task, esse_content, esse_result, date) VALUES (?, ?, ?, ?, datetime('now'))", (login, esse_task, esse_content, esse_result))
        self.db.commit()
    
    def can_use(self, login: str):
        result = self.db.execute("SELECT tokens FROM users WHERE login = ?", (login,))
        user = result.fetchone()
        if user[0] > 0:
            return True
        return False
    
    def is_admin(self, login: str):
        result = self.db.execute("SELECT admin FROM users WHERE login = ?", (login,))
        user = result.fetchone()
        if user[0]:
            return True
        else:
            return False
    
    def add_user_tokens(self, username, tokens):
        self.db.execute("UPDATE users SET tokens = tokens + ? WHERE login = ?", (tokens, username))
        self.db.commit()

    
    def get_users(self):
        response = self.db.execute("SELECT * from users")
        result = response.fetchall()
        users = []
        for i in result:
            users.append(i[1])
        return users
    
    def get_user(self, username):
        response = self.db.execute("SELECT login, tokens, admin, esse_checks from users WHERE login = ?", (username,))
        result = response.fetchall()
        if result == []:
            return None
        user = {'login': result[0][0], 'tokens': result[0][1], 'admin': result[0][2], 'esse_checks': result[0][3]}
        return user

    def get_user_tokens(self, username):
        result = self.db.execute("SELECT tokens FROM users WHERE login = ?", (username,))
        user = result.fetchone()
        return user[0]
    
    def get_user_checks(self, username):
        result = self.db.execute("SELECT esse_checks FROM users WHERE login = ?", (username,))
        user = result.fetchone()
        return user[0]
    
    def get_user_last_activity(self, username):
        result = self.db.execute("SELECT last_activity FROM users WHERE login = ?", (username,))
        user = result.fetchone()
        return user[0]

    def get_user_info(self, username):
        result = self.db.execute("SELECT * FROM users WHERE login = ?", (username,))
        user = result.fetchone()
        return [user[3], user[5], user[6]]

    def get_user_esses_list(self, username):
        result = self.db.execute("SELECT * FROM logs WHERE login = ?", (username,))
        buf = []
        esses = result.fetchall()
        for i in esses:
            buf.append(i[5])
        print(buf)
        return buf
    
    def get_all_user_esses(self, username):
        result = self.db.execute("SELECT date FROM logs WHERE login = ?", (username,))
        esses = result.fetchall()
        buf = []
        for i in esses:
            buf.append(i[0])
        return buf

    def get_esse(self, username, esse_date):
        result = self.db.execute("SELECT * FROM logs WHERE login = ? AND date = ?", (username, esse_date))
        esse = result.fetchone()
        return [esse[2], esse[3], esse[4]]
