from langchain_openai import ChatOpenAI
from langchain.chains.router.llm_router import LLMRouterChain
from langchain.chains import create_sql_query_chain
from langchain.chains.llm import LLMChain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities import SQLDatabase
import sqlite3
import os
import time
from .response import OUTPUT_TEMPLATES
from mulyank.prompt_builder import QueryBuilder, RouterBuilder, OUTPUT_PROMPT


class OutputFormatter:

    def __init__(self, destination_key):
        self.template = OUTPUT_TEMPLATES[destination_key][0]
        self.aggregation = OUTPUT_TEMPLATES[destination_key][1]

    def apply(self, agg, res):
        if agg == "add":
            return sum(res)
    
    def format(self, response):
        print(response)
        if self.aggregation != None:
            response = [[self.apply(self.aggregation, response[0])]]
        inputs = {key:val for key, val in zip(self.template.input_variables, response[0])}
        return self.template.format(**inputs)

class QueryHandler:

    def __init__(self, api_key, db_loc = "sqlite:///db/mulyank.db"):
        llm = ChatOpenAI(api_key=api_key, temperature=0,seed = 0)
        query_bldr = QueryBuilder()
        router_bldr = RouterBuilder()
        db = SQLDatabase.from_uri(db_loc)
        self.write_query = create_sql_query_chain(llm, db)
        self.router_chain = LLMRouterChain.from_llm(llm, router_bldr.get_router_prompt())
        self.query_mapping = query_bldr.get_query_mapping()
        self.basic_question_list = ["greetings","mulyankan_working","event_handling" ,"future_question"]
        self.output_chain = LLMChain(llm = llm, prompt=OUTPUT_PROMPT)


    def format_response(self, response, destination_key):
        if destination_key in self.basic_question_list:
            return response
        else:
            return OutputFormatter(destination_key).format(response)


    def run_query(self, sql_query):
        conn = sqlite3.connect("db/mulyank.db")
        c = conn.cursor()
        c.execute(sql_query)
        response = c.fetchall()
        conn.commit()
        conn.close()
        return response
        
    def handle_questions(self, state):
        try:
            user_message = state.messages[-1]["content"].lower()
            destination_key = self.router_chain.invoke({"input": user_message})["destination"]
            query = self.query_mapping[destination_key]
            if type(query) != str:
                query = query.format(question = user_message)
                sql_query = self.write_query.invoke({"question": query})
                sql_query = sql_query.replace("```","")
                print("*******")
                print(sql_query)
                print("*******")
                
                response = self.run_query(sql_query)
                response = self.format_response(response, destination_key)
                response = self.output_chain.invoke(input = {"query" : user_message, "response" : response})["text"]
            else:
                response = self.query_mapping[destination_key]
                response = self.format_response(response, destination_key)

            
        except:
            response = "I am sorry, I couldn't respond to this question at this time. Stay Tuned for MULYANKAN GPT updates."

        for word in response.split("\n"):
            time.sleep(0.05)
            yield word + "\n"
