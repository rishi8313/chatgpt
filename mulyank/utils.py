
from .core import QueryHandler
import os
from dotenv import load_dotenv

if not load_dotenv("/etc/secrets/.env"):
    load_dotenv("mulyank/etc/secrets/.env")

qh = None

def generate_response(state):
    global qh
    if qh == None:
        qh = QueryHandler(api_key=os.environ["OPENAI_API_KEY"], db_loc=os.environ["DB_CONNECTION_STR"])
    if response := qh.handle_questions(state):
        return response
    

