
from .core import QueryHandler
import os
from dotenv import load_dotenv
load_dotenv("/etc/secrets/.env")

qh = QueryHandler(api_key=os.environ["OPENAI_API_KEY"])

def generate_response(state):

    if response := qh.handle_questions(state):
        return response
    

