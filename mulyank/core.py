from langchain_openai import ChatOpenAI
from langchain.chains.router.llm_router import LLMRouterChain
from langchain.chains import create_sql_query_chain
from langchain.chains.llm import LLMChain
from langchain_community.utilities import SQLDatabase
from langchain_community.cache import InMemoryCache
from langchain.globals import set_llm_cache
import time
from .response import OUTPUT_TEMPLATES
from mulyank.prompt_builder import QueryBuilder, RouterBuilder, OUTPUT_PROMPT, IN_PROMPT, DIRECT_PROMPT
from sqlalchemy import create_engine
from sqlalchemy import text
from langchain.callbacks.base import BaseCallbackHandler
from datetime import datetime
set_llm_cache(InMemoryCache())


DEBUG = True

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

class OutputFormatter:

    def __init__(self, destination_key):
        if destination_key in OUTPUT_TEMPLATES.keys():
            self.template = OUTPUT_TEMPLATES[destination_key][0]
            self.aggregation = OUTPUT_TEMPLATES[destination_key][1]
            self.formatting_needed = True
        else:
            self.formatting_needed = False

    def apply(self, agg, res):
        if DEBUG:
            print(res)
        if agg == "convert_to_perc":
            return (res[0], res[1], float(res[2])*100, 
                    float(res[3])*100, res[4], res[5])
        elif agg == "divide_by_10000":
            out = []
            for val in res:
                out.append(float(val)/10000)
            return tuple(out)
        elif agg == "multiply_100":
            return (res[0], float(res[1])*100, res[2], res[3])
        elif agg == "add":
            return sum(res)
        elif agg == "frac":
            return (int(res[0]*100), res[1], res[2])
        elif agg == "frac_aggr":
            out = [int(res[0]*100), int(res[1] * 100), int(res[2]*100)]
            out.extend(res[3:])
            return out
        elif agg == "all":
            return str(res)
        elif agg == "concat":
            print("I am inside concate", res)
            concatenated = ""
            for r in res:
                concatenated += r[0]
            return concatenated
        elif agg == "concat_perf":
            return res
    
    def format(self, response):
        if DEBUG:
            print(response)
        if self.aggregation != None:
            if self.aggregation not in ["concat", "all"]:
                agg_resp = self.apply(self.aggregation, response[0])
            else:
                agg_resp = self.apply(self.aggregation, response)
            if type(agg_resp) is str or type(agg_resp) is int or type(agg_resp) is float:
                response = [[agg_resp]]
            elif type(agg_resp) is tuple or type(agg_resp) is list:
                response = [agg_resp]
        if DEBUG:
            print(self.template.input_variables)
        inputs = {key:val for key, val in zip(self.template.input_variables, response[0])}
        if DEBUG:
            print(inputs)
        return self.template.format(**inputs)

class QueryHandler:

    def __init__(self, api_key, db_loc = "sqlite:///db/mulyank.db"):
        llm = ChatOpenAI(model = "gpt-4o-mini-2024-07-18",api_key=api_key, temperature=0, max_tokens=40)
        self.llm = ChatOpenAI(model = "gpt-4o-mini-2024-07-18", api_key=api_key, temperature=0, max_tokens=256)
        self.llm_gpt4o = ChatOpenAI(model = "gpt-4o",api_key=api_key, temperature=0)
        self.translate_chain = LLMChain(llm = llm, prompt=IN_PROMPT)
        query_bldr = QueryBuilder()
        self.db_connection_str = db_loc
        router_bldr = RouterBuilder()
        self.router_chain = LLMRouterChain.from_llm(llm, router_bldr.get_router_prompt())
        self.query_mapping = query_bldr.get_query_mapping()
        llm1 = ChatOpenAI(model = "gpt-4o-mini-2024-07-18",api_key=api_key, temperature=0.3)
        self.output_chain = LLMChain(llm = llm1, prompt=OUTPUT_PROMPT)

    def run_query(self, sql_query):
        response = "Not able to connect to mulyankan database at this moment"
        engine = create_engine(self.db_connection_str)
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            response = result.fetchall()
        return response
        
    def handle_questions(self, state):
        
        try:
            user_message = state.messages[-1]["content"].lower()
            if DEBUG:
                print(user_message)
            print("start_time",datetime.now())
            user_message = self.translate_chain.invoke(input = {"message": user_message})["text"]
            print("translate time",datetime.now())
            if DEBUG:
                print(user_message)
            destination_key = self.router_chain.invoke({"input": user_message})["destination"]
            print("router_time",datetime.now())
            if DEBUG:
                print(destination_key)
            query = self.query_mapping[destination_key]
            print(type(query))
            if type(query) == str:
                response = self.query_mapping[destination_key]
            elif type(query) == tuple and query[0] == "direct":
                direct_chain = LLMChain(llm = self.llm_gpt4o, prompt=DIRECT_PROMPT)
                response = direct_chain.invoke(input = {"query" : user_message})["text"]
            elif type(query) == tuple:
                sql_chain_input = query[1].format(question = user_message)
                db = SQLDatabase.from_uri(self.db_connection_str)
                write_query = create_sql_query_chain(self.llm, db)
                print("chain_creation_time", datetime.now())
                sql_query = write_query.invoke({"question": sql_chain_input})
                print("query generation time", datetime.now())
                sql_query = sql_query.replace("```","")
                sql_query = sql_query.replace("sql\n","")
                sql_query = sql_query.strip()
                sql_query = sql_query[sql_query.find("SELECT"):]
                if DEBUG:
                    print("*******")
                    print(sql_query)
                    print("*******")
                
                response = self.run_query(sql_query)
                if DEBUG:
                    print(destination_key)
                if query[0] == "prompt_helper":
                    response = OutputFormatter(destination_key).format(response)
                    response = self.output_chain.invoke(input = {"query" : user_message, "response" : response})["text"]
                elif query[0] == "direct_to_sql_chain":
                    if OutputFormatter(destination_key).formatting_needed == True:
                        response = OutputFormatter(destination_key).format(response)
                        response = self.output_chain.invoke(input = {"query" : user_message, "response" : response})["text"]
                    else:
                        print(response)
                        response = self.output_chain.invoke(input = {"query" : user_message, "response" : str(response)})["text"]
        except:
           response = "I am sorry, I couldn't respond to this question at this time. Stay Tuned for MULYANKAN GPT updates."

        for sentence in response.split("\n"):
            for word in sentence.split(" "):
                time.sleep(0.0001)
                yield word + " "
            yield "\n"
