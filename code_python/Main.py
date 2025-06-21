from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

print(os.getenv("MONGO_DB_HOST"))
print(os.getenv("REDIS_PORT"))
print(os.getenv("REDIS_HOST"))