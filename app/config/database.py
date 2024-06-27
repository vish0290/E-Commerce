from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
try:
	client = MongoClient(f"mongodb+srv://{db_user}:{db_pass}@cluster0.tbg2bb1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
	db = client.ecom
	user_db = db['user']
	product_db = db['product']
	category_db = db['category']
	seller_db = db['seller']
	admin_db = db['admin']
	order_db = db['order']
	cart_db = db['cart']
except Exception as e:
	print(f"Error connecting to MongoDB: {str(e)}")