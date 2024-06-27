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

def seller_serial(seller) -> dict:
    return {    
        "name": seller['name'],
        "email": seller['email'],
        'password': seller['password'],
        'phone': seller['phone']
    }
    
def list_seller(sellers) -> list:
    return [seller_serial(seller) for seller in sellers]

def admin_serial(admin) -> dict:
    return {    
        "username": admin['username'],
        'password': admin['password']
    }
    
def category_serial(category) -> dict:
    return {    
        "name": category['name'],
        'description': category['description'],
        'last_change': category['last_change']
    }

def list_category(categories) -> list:
    return [category_serial(category) for category in categories]