CREATE_USERS = """CREATE TABLE users (
                  user_id INTEGER PRIMARY KEY, 
                  first_name TEXT NOT NULL, 
                  last_name TEXT NOT NULL, 
                  status TEXT DEFAULT 'welcome')"""

CREATE_DATA = """CREATE TABLE data (
                 user_id INTEGER PRIMARY KEY, 
                 vars TEXT, 
                 func TEXT, 
                 interval_x TEXT, 
                 interval_y TEXT, 
                 g_func TEXT, 
                 restr TEXT, 
                 FOREIGN KEY(user_id) REFERENCES users(user_id))"""

INSERT_USERS = "INSERT INTO users(user_id, first_name, last_name) VALUES (?, ?, ?)"

INSERT_DATA = "INSERT INTO data(user_id) VALUES (?)"

UPDATE_USERS = "UPDATE users SET status = ? WHERE user_id = ?"

UPDATE_DATA = "UPDATE data SET {} = ? WHERE user_id = ?"
