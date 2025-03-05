# utils/env_variables.py

import os

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file


def load_env_variables():
    return {
        # Neo4j configuration variables
        'NEO4J_URI': os.getenv('NEO4J_URI'),
        'NEO4J_DATABASE': os.getenv('NEO4J_DATABASE'),
        'NEO4J_USER': os.getenv('NEO4J_USER'),
        'NEO4J_PASSWORD': os.getenv('NEO4J_PASSWORD'),
        'NEO4J_DATABASE_VECTOR_INDEX': os.getenv('NEO4J_DATABASE_VECTOR_INDEX'),

        # OpenAI configuration variables
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'OPENAI_MODEL': os.getenv('OPENAI_MODEL'),
        'OPENAI_MODEL_TEMPERATURE': os.getenv('OPENAI_MODEL_TEMPERATURE'),
    }
