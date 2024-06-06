
from .core import QueryHandler
import os
from dotenv import load_dotenv

if not load_dotenv("/etc/secrets/.env"):
    load_dotenv("mulyank/etc/secrets/.env")

qh = QueryHandler(api_key=os.environ["OPENAI_API_KEY"])

def generate_response(state):
    try:
        if response := qh.handle_questions(state):
            return response
    

