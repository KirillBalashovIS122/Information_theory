"""
Модуль для управления базой данных пользователей.

Этот модуль предоставляет функции для создания базы данных,
добавления, удаления и изменения пользователей,
а также для хеширования паролей.

Функции:
- create_database(): Создает базу данных и необходимые таблицы (User_types, Users).
- hash_password(password): Хеширует пароль методом MD5.
- get_all_users(): Возвращает список всех пользователей.
- add_user(login, password, utype_id): Добавляет нового пользователя в базу данных.
- get_user_by_login(login): Возвращает пользователя по логину.
- delete_user_by_login(login): Удаляет пользователя из базы данных по логину.
- change_user_password(login, new_password): Изменяет пароль пользователя.

Константы:
- DB_PATH: Путь к файлу базы данных.

Примечание:
Внимание! В целях безопасности реальные пароли пользователей не должны храниться в открытом виде.
Они хранятся в базе данных в виде хэш-суммы (MD5).
"""
import os
import sqlite3
import hashlib

DB_PATH = 'base2.db'

def create_database():
    """
    Создает базу данных и необходимые таблицы.

    Если база данных уже существует, она будет удалена и создана заново.
    Таблицы User_types и Users будут созданы, если их не существует.
    """
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
    """
    Хеширует пароль методом MD5.

    Args:
    - password: Пароль для хеширования.

    Returns:
    - Хэш-сумма пароля в виде строки.
    """
    hash_md5 = hashlib.md5()
    hash_md5.update(password.encode())
    return hash_md5.hexdigest()

def get_all_users():
    """
    Возвращает список всех пользователей.

    Returns:
    - Список всех пользователей в виде списка кортежей.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT login FROM Users")
    all_users = cursor.fetchall()
    cursor.close()
    return all_users


def add_user(login, password, utype_id):
    """
    Добавляет нового пользователя в базу данных.

    Args:
    - login: Логин нового пользователя.
    - password: Пароль нового пользователя.
    - utype_id: Идентификатор типа пользователя (1 для администратора, 2 для пользователя).
    """
    hashed_password = hash_password(password)
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Users (login, password, utype_id) VALUES (?,?,?);",
                    (login, hashed_password, utype_id))
        connection.commit()
        cursor.close()
        print("Пользователь добавлен в базу данных")
    except sqlite3.Error as error:
        print("Ошибка при добавлении пользователя:", error)
    finally:
        if connection:
            connection.close()

def get_user_by_login(login):
    """
    Возвращает пользователя по логину.

    Args:
    - login: Логин пользователя.

    Returns:
    - Кортеж с информацией о пользователе или None, если пользователь не найден.
    """
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
    """
    Удаляет пользователя из базы данных по логину.

    Args:
    - login: Логин пользователя.
    """
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
    """
    Изменяет пароль пользователя.

    Args:
    - login: Логин пользователя.
    - new_password: Новый пароль.
    """
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
