import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Redis
    REDIS_HOST = os.getenv('REDIS_HOST', '147.93.3.53')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = "gpt-4-turbo-preview"  # Or gpt-3.5-turbo if preferred
    EMBEDDING_MODEL = "text-embedding-3-small"

    # App
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    TOP_K = 3
