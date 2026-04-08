import sqlite3

def sanitize_table_name(user_id):
    if not user_id:
        return None 
    return f"messages_user_{str(user_id)}"
##Following function initializes tables for users
def init_user_table(user_id):
    table_name=sanitize_table_name(user_id)
    if not table_name:
        return
    connection=sqlite3.connect("messages_tele.db")
    c=connection.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name}(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              message_id INTEGER UNIQUE,
              user_id INTEGER,
              text TEXT,
              timestamp TEXT,
              from_me BOOLEAN
              )''')
    connection.commit()
    connection.close()
##Following functions clears the user tables
def clear_table(user_id):
    table_name=sanitize_table_name(user_id)
    if not table_name:
        return
    connection=sqlite3.connect("messages_tele.db")
    c=connection.cursor()
    c.execute(f'''DELETE FROM {table_name}''')
    connection.commit()
    connection.close()
##Following function inserts messages in the database
def insert_user_message(user_id, message_id, sender_id, text, timestamp, from_me):
    table_name=sanitize_table_name(user_id)
    if not table_name:
        return
    connection=sqlite3.connect("messages_tele.db")
    c=connection.cursor()
    c.execute(f'''INSERT OR IGNORE INTO {table_name}(message_id, user_id, text, timestamp, from_me)
              VALUES (?,?,?,?,?)''', (message_id, sender_id, text, timestamp, from_me))
    connection.commit()
    connection.close()