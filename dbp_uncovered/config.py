import os
from dotenv import load_dotenv


load_dotenv() #To take the environment variables from the .env file

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port':     int(os.getenv('DB_PORT', 3306)),
    'user':     os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}
