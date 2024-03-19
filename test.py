from db import DataBase

db= DataBase()

date =  db.get_all_user_esses("root")[0]
print(db.get_esse("root", date))