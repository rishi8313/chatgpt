from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains.router.llm_router import LLMRouterChain
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
import sqlite3
import os
import time
from .prompts import router_prompt,query_mapping
from .response import OUTPUT_TEMPLATES

load_dotenv()

class OutputFormatter:

    def __init__(self, destination_key):
        self.template = OUTPUT_TEMPLATES[destination_key]

    def format(self, response):
        inputs = {key:val for key, val in zip(self.template.input_variables, response[0])}
        print(inputs)
        return self.template.format(**inputs)

class QueryHandler:

    def __init__(self, api_key, db_loc = "sqlite:///db/mulyank.db"):
        llm = ChatOpenAI(api_key=api_key)
        db = SQLDatabase.from_uri(db_loc)
        self.write_query = create_sql_query_chain(llm, db)
        self.router_chain = LLMRouterChain.from_llm(llm, router_prompt)
        self.query_mapping = query_mapping
        self.basic_question_list = ["greetings","mulyankan_working","event_handling" ,"future_question"]


    def format_response(self, response, destination_key):
        if destination_key in self.basic_question_list:
            return response
        else:
            return OutputFormatter(destination_key).format(response)

    def handle_questions(self, state):
        user_message = state.messages[-1]["content"].lower()
        destination_key = self.router_chain.invoke({"input": user_message})["destination"]
        query = self.query_mapping[destination_key]
        if type(query) != str:
            query = query.format(question = user_message)
            sql_query = self.write_query.invoke({"question": query})
            print(sql_query)
            conn = sqlite3.connect("db/mulyank.db")
            c = conn.cursor()
            c.execute(sql_query)
            response = c.fetchall()
            conn.commit()
            conn.close()
        else:
            response = self.query_mapping[destination_key]

        response = self.format_response(response, destination_key)

        for word in response.split():
            time.sleep(0.05)
            yield word + " "
