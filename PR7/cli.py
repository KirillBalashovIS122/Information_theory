"""
Программа управления пользователями.

Эта программа предоставляет интерфейс для аутентификации, администрирования
и управления пользователями через командную строку.

Функции:
- admin_menu(): Меню администратора для просмотра, добавления, удаления пользователей
и изменения паролей.
- user_menu(): Меню пользователя для изменения собственного пароля.
- main(): Главная функция программы, которая обеспечивает интерфейс входа, 
регистрации и управления программой.

Импортированные функции из других модулей:
- authenticate_user: Функция аутентификации пользователя.
- authorize_user: Функция авторизации пользователя.
- create_database: Функция создания базы данных.
- add_user: Функция добавления нового пользователя.
- get_all_users: Функция получения списка всех пользователей.
- delete_user_by_login: Функция удаления пользователя по логину.
- change_user_password: Функция изменения пароля пользователя.

Примечание:
Программа предполагает, что существует база данных и пользователь "admin" с паролем "admin",
который имеет права администратора.
"""

from authentication import authenticate_user, authorize_user
from database import create_database, add_user, get_all_users
from database import delete_user_by_login, change_user_password


def admin_menu():
    """
    Меню администратора.
    
    Позволяет администратору просматривать, добавлять, удалять пользователей и менять пароли.
    """
    while True:
        print("\nМеню администратора:")
        print("1. Вывести список пользователей")
        print("2. Удалить пользователя")
        print("3. Добавить нового пользователя")
        print("4. Сменить свой пароль")
        print("5. Выйти из учетной записи администратора")

        choice = input("Введите номер действия: ")

        if choice == "1":
            print(get_all_users())
        elif choice == "2":
            login = input("Введите логин пользователя для удаления: ")
            delete_user_by_login(login)
        elif choice == "3":
            login = input("Введите логин нового пользователя: ")
            password = input("Введите пароль нового пользователя: ")
            user_type = input("Введите тип пользователя (1 для администратора,2 для пользователя):")
            add_user(login, password, user_type)
        elif choice == "4":
            login=input("Введите свой логин")
            new_password = input("Введите новый пароль: ")
            change_user_password(login, new_password)
        elif choice == "5":
            print("Выход из учетной записи администратора.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


def user_menu():
    """
    Меню пользователя.
    
    Позволяет пользователю изменить свой пароль.
    """
    while True:
        print("\nМеню пользователя:")
        print("1. Сменить свой пароль")
        print("2. Выйти из программы")
        choice = input("Введите номер действия: ")
        if choice =="1":
            login=input("Введите свой логин: ")
            new_password = input("Введите новый пароль: ")
            change_user_password(login,new_password)
        elif choice =="2":
            break
        else:
            print("Неккоректный ввод, попробуйте снова.")


def main():
    """
    Главная функция программы.
    
    Обеспечивает интерфейс входа, регистрации и управления программой.
    """
    print("Добро пожаловать в программу управления пользователями.")
    create_database()
    add_user("admin", "admin", 1)

    while True:
        print("\nВыберите действие:")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("3. Выйти из программы")

        choice = input("Введите номер действия: ")

        if choice == "1":
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            authenticated, user_type = authenticate_user(login, password)
            if authenticated:
                authorize_user(user_type)
                if user_type == 1:
                    admin_menu()
                elif user_type == 2:
                    user_menu()
                else:
                    print("Некорректный тип пользователя.")
            else:
                print("Ошибка аутентификации. Попробуйте снова.")
        elif choice == "2":
            login=input("Введите логин: ")
            password=input("Введите пароль: ")
            add_user(login,password,2)

        elif choice == "3":
            print("До свидания!")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()
