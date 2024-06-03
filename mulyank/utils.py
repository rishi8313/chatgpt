
from .core import QueryHandler
import os

qh = QueryHandler(api_key=os.environ["OPENAI_API_KEY"])

def generate_response(state):

    if response := qh.handle_questions(state):
        return response
    

