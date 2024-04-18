from database import get_user_by_login, hash_password

def authenticate_user(login, password):
    user = get_user_by_login(login)
    if user:
        hashed_password = hash_password(password)
        if user[2] == hashed_password:
            return True, user[3]  # Возвращаем True и ID типа пользователя
    return False, None

def authorize_user(user_type):
    if user_type == 1:
        return "Вы авторизованы с правами администратора."
    elif user_type == 2:
        return "Вы авторизованы с правами пользователя."
    else:
        return "Некорректный тип пользователя."
