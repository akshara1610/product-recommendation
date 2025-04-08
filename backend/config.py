import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings
config = {
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'MODEL_NAME': os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
    'MAX_TOKENS': int(os.getenv('MAX_TOKENS', 1000)),
    'TEMPERATURE': float(os.getenv('TEMPERATURE', 0.7)),
    'DATA_PATH': os.getenv('DATA_PATH', 'data/products.json'),
    'USE_CACHE': os.getenv('USE_CACHE',True),
    'CACHE_DIR': os.getenv('CACHE_DIR', 'cache'),
    'CACHE_TTL_HOURS': os.getenv('CACHE_TTL_HOURS',24)
}