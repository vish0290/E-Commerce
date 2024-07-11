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
        "id": str(seller["_id"]),    
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
        "id": str(category["_id"]),    
        "name": category['name'],
        'description': category['description'],
        'image': category['image'],
        'last_change': category['last_change']
    }

def list_category(categories) -> list:
    return [category_serial(category) for category in categories]

def product_serial(product) -> dict:
    return {   
        "id": str(product["_id"]),
        "name": product['name'],
        'images': product['images'],
        'price': product['price'],
        'base_feature': product['base_feature'],
        'stock': product['stock'],
        'description': product['description'],
        'stock': product['stock'],
        'cat_id': product['cat_id'],
        'seller_id': product['seller_id'],
        'last_change': product['last_change']
    }

def list_product(products) -> list:
    return [product_serial(product) for product in products]


def order_serial(order) -> dict:
    return {    
        "id": str(order["_id"]),
        "user_id": order['user_id'],
        'product_data': order['product_data'],
        'total_price': order['total_price'],
        'last_change': order['last_change'],
    }

def list_order(orders) -> list:
    return [order_serial(order) for order in orders]

def cart_serial(cart) -> dict:
    return {    
        "id": str(cart["_id"]),
        "user_id": cart['user_id'],
        'product_data': cart['product_data'],
        'total_price': cart['total_price'],
        'last_change': cart['last_change']
    }
    
def list_cart(carts) -> list:
    return [cart_serial(cart) for cart in carts]