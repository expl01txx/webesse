import sqlite3

class DataBase:
    def __init__(self):
        self.db = sqlite3.connect("db/webesse.db")
    def auth(self, login: str, passwd: str) -> bool:
        try:
            result = self.db.execute("SELECT * FROM users WHERE login = ? AND passwd = ?", (login, passwd))
            if result.fetchone():
                return True
            else:
                return False
        except:
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
        result = self.db.execute("SELECT * FROM users WHERE login = ?", (login,))
        user = result.fetchone()
        if user[3] > 0:
            return True
        return False
    
    def is_admin(self, login: str):
        result = self.db.execute("SELECT * FROM users WHERE login = ?", (login,))
        user = result.fetchone()
        if user[4]:
            return True
        else:
            return False
    
    def get_users(self):
        response = self.db.execute("SELECT * from users")
        result = response.fetchall()
        users = []
        for i in result:
            users.append(i[1])
        return users
    
    def get_user_tokens(self, username):
        result = self.db.execute("SELECT * FROM users WHERE login = ?", (username,))
        user = result.fetchone()
        return user[4]
    
    def add_user_tokens(self, username, tokens):
        self.db.execute("UPDATE users SET tokens = tokens + ? WHERE login = ?", (tokens, username))
        self.db.commit()
    
    def get_user_checks(self, username):
        result = self.db.execute("SELECT * FROM users WHERE login = ?", (username,))
        user = result.fetchone()
        return user[6]
    
    def get_user_last_activity(self, username):
        result = self.db.execute("SELECT * FROM users WHERE login = ?", (username,))
        user = result.fetchone()
        return user[7]

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