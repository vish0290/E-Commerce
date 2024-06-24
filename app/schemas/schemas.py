def user_serial(user) -> dict:
    return {    
        "id": str(user["_id"]),
        "name": user['name'],
        "email": user['email'],
        'password': user['password'],
        "address": user['address'],
        'last_login': user['last_login']
    }


def list_user(users) -> list:
    return [user_serial(user) for user in users]