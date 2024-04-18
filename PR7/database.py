import os
import sqlite3
import hashlib

DB_PATH = 'base2.db'

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS User_types (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            utype TEXT NOT NULL UNIQUE);''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            login TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            utype_id INTEGER,
                            FOREIGN KEY (utype_id) REFERENCES User_types(id) 
                            ON DELETE CASCADE);''')

        records = [('Администратор',),
                   ('Пользователь',)]
        cursor.executemany("INSERT INTO User_types (utype) VALUES (?);", records)

        connection.commit()
        cursor.close()
        print("База данных создана и заполнена")
    except sqlite3.Error as error:
        print("Ошибка при работе с базой данных:", error)
    finally:
        if connection:
            connection.close()

def hash_password(password):
    hash_md5 = hashlib.md5()
    hash_md5.update(password.encode())
    return hash_md5.hexdigest()
def get_all_users():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT login FROM Users")
    all_user=cursor.fetchone()
    cursor.close()
    return all_user
def add_user(login, password, utype_id):
    hashed_password = hash_password(password)
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Users (login, password, utype_id) VALUES (?,?,?);", (login, hashed_password, utype_id))
        connection.commit()
        cursor.close()
        print("Пользователь добавлен в базу данных")
    except sqlite3.Error as error:
        print("Ошибка при добавлении пользователя:", error)
    finally:
        if connection:
            connection.close()

def get_user_by_login(login):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Users WHERE login=?", (login,))
        user = cursor.fetchone()

        cursor.close()
        return user
    except sqlite3.Error as error:
        print("Ошибка при поиске пользователя:", error)
        return None
    finally:
        if connection:
            connection.close()
def delete_user_by_login(login):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Users WHERE login=?", (login,))
        connection.commit()
        cursor.close()
        print("Пользователь удален из базы данных")
    except sqlite3.Error as error:
        print("Ошибка при удалении пользователя:", error)
    finally:
        if connection:
            connection.close()

def change_user_password(login, new_password):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        hashed_password = hash_password(new_password)
        cursor.execute("UPDATE Users SET password=? WHERE login=?", (hashed_password, login))
        connection.commit()
        cursor.close()
        print("Пароль пользователя изменен")
    except sqlite3.Error as error:
        print("Ошибка при изменении пароля:", error)
    finally:
        if connection:
            connection.close()
