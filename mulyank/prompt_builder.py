from json import JSONDecoder
from langchain.prompts import PromptTemplate
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains.router.llm_router import RouterOutputParser

# PROMPT_PREFIX = """Answer the following question

# {question}

# While creating the sql query, remember the following points
# Remember : Always convert date provided in the question to datetime sql type while generating sql query.
# Remember : Always use strftime date time matching for dates.
# Remember : use the latest date present in database convert it to strftime format to match, If date, month or year is not mentioned in the question, 
# Remember : If only month and year is mentioned, then take an Mean of whole month for the given year and provide the value
# Remember : If only year is mentioned, then take an average of whole year and provide the value
# Remember : If data, month and year all 3 are mentioned, then get the value for the exact date from the date column which is a datetime type column
# Remember : To round off the values upto 2 decimal points only.
# by providing the following information.

# """
PROMPT_PREFIX = """
Create an SQL query that adheres to these guidelines:

##Important Guidelines to follow
1. Never order by index, always use date of ordering.
2. Whenever a question includes a date, always convert that date to the datetime format using SQL's DATEFORMAT function to ensure consistency in date matching.
3. If date is not provided in the question, consider it as latest scenario and append "current" keyword to the question. 
eg. a) Which category to select under equity? -> Currently which category to select under equity.
    b) Which category to select under equity in Jan 2023? -> Which category to select under equity in Jan 2023?
4. If the date (day, month, year) isn’t fully specified:
   - Use the latest date in the database in the `strftime` format. Refrain to use date('now') to get the latest date.
   - If only the month and year are mentioned, compute the mean value for the entire month in the specified year.
   - If only the year is mentioned, calculate the average value for the entire year.
   - If the full date (day, month, and year) is provided, extract the value for the precise date from the datetime column.
5. If the question starts with "when", strictly refrain to select date as column, you could still use date in filter or for ordering purpose
Provide the information as requested:

{question}

"""

DIRECT_SQL_PROMPT = """
Create an SQL query that adheres to these guidelines:

1) When filter on Equity funds, remember following are the equity fund categories
Equity - Focused Fund
Equity - Dividend Yield Fund
Equity - ELSS
Equity - Large & Mid Cap Fund
Equity - Thematic Fund - Other
Equity - Flexi Cap Fund
Equity - Large Cap Fund
Equity - Mid Cap Fund
Index Funds - Other
Index Funds - Nifty
Index Funds - Nifty Next 50
Equity - Value Fund
Equity - Small cap Fund
Equity - Multi Cap Fund
Equity - Sectoral Fund - Service Industry
Index Funds - Sensex
Equity - Contra Fund

2) When filter on Hybrid funds, remember following are the hybrid fund categories
Hybrid - Arbitrage Fund
Hybrid - Balanced Advantage
Hybrid - Aggressive Hybrid Fund
Hybrid - Equity Savings
Hybrid - Conservative Hybrid Fund
Hybrid - Multi Asset Allocation
Hybrid - Dynamic Asset Allocation

3) When filter on Debt funds, remember following are the debt fund categories
Debt - Banking and PSU Fund
Debt - Corporate Bond Fund
Debt - Credit Risk Fund
Debt - Dynamic Bond
Debt - Floater Fund
Debt - Gilt Fund
Debt - Medium to Long Duration Fund
Debt - Liquid Fund
Debt - Low Duration Fund
Debt - Medium Duration Fund
Debt - Money Market Fund
Debt - Ultra Short Duration Fund
Debt - Short Duration Fund
Debt - Gilt Fund with 10 year constant duration
Debt - Long Duration Fund

4) Do not apply limit on the sql query e.g. LIMIT 5 or LIMIT 10. It is not required.

5) When filtering the data on string columns, use approximate match rather than full match. Do not filter on past tactical calls.

6) use exact match for mid cap fund, Nifty fund, gilt fund and long duration fund. 

7) when scheme name is present in the question, 
 a) strictly include it in the query for approximate matching in lower case, (split the scheme name in different words and match)
 b) strictly include the type of scheme eg. corporate or baf or mid cap etc. as an AND condition
 c) Also try for large cap when asked for bluechip category
 d) Use Balance advantage fund as category in place of BAF
{question}

"""

class QueryBuilder:

    def __init__(self, 
                 prompt_config_file_path = "configs/template_config.json", 
                 query_def_file_path = "configs/query_definitions.json"):
        
        with open(prompt_config_file_path) as f:
            decoder = JSONDecoder()
            content = decoder.decode(f.read())

        with open(query_def_file_path) as f:
            decoder = JSONDecoder()
            self.query_def_content = decoder.decode(f.read())

        self.build(content)

    def get_prompt(self, template):
        return PromptTemplate(
        template=template,
        input_variables=["question"],
        output_parser=None
    )

    def manage_block(self, block):
        columns = block["columns"]
        table_name = block["table_name"]
        prefix = block["prefix"]
        columns_str = ", ".join(columns)
        mid_sec = " from "
        template = PROMPT_PREFIX + "\n" + prefix + " " + columns_str + mid_sec + table_name
        return template

    def handle_predefined(self, name):
        return self.query_def_content[name]
    
    def handle_direct_query(self, name):
        block = self.query_def_content[name]
        table_name = block["table_name"]

        template = DIRECT_SQL_PROMPT 
        if "prefix" in block.keys():
            prefix = block["prefix"]
            template += "\n {}".format(prefix)
        if "columns" in block.keys():
            columns = block["columns"]
            columns_str = ", ".join(columns)
            template += " {} only".format(columns_str)
        template += "\n" + "use table name : " + table_name
        if "filter_by" in block.keys():
            filter_column = block["filter_by"]
            template += " \napply filter : {}".format(filter_column)
        return self.get_prompt(template)
        
    def handle_prompt_helper(self, name):
        block = self.query_def_content[name]
        template = self.manage_block(block)
        return self.get_prompt(template)

    def build(self, content):
        self.query_mapping = {}
        for block in content["prompt_infos"]:
            name = block["name"]
            if block["kind"] == "Predefined":
                self.query_mapping[name] = self.handle_predefined(name)
            elif block["kind"] == "direct":
                self.query_mapping[name] = (block["kind"], name)
            elif block["kind"] == "direct_to_sql_chain":
                self.query_mapping[name] = (block["kind"], self.handle_direct_query(name))
            else:
                self.query_mapping[name] = (block["kind"], self.handle_prompt_helper(name))

    def get_query_mapping(self):
        return self.query_mapping


class RouterBuilder:

    def __init__(self, prompt_config_file_path = "configs/template_config.json"):
        with open(prompt_config_file_path) as f:
            decoder = JSONDecoder()
            content = decoder.decode(f.read())

        self.create_router_prompt(content)

    def create_router_prompt(self, content):
        prompt_infos = content["prompt_infos"]
        destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
        destinations_str = "\n".join(destinations)

        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
            destinations=destinations_str
        )

        self.router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(),
        )

    def get_router_prompt(self):
        return self.router_prompt
    

out_template = """ ### Tips for Crafting a Human-Readable Response: ###

- Use a conversational tone that is easy to comprehend
- Adjust the calculations according to the query
- Clearly present any numerical or factual information in bulletpoints, always use Indian currency system
- seperate the facts by next line character ("\n")
- encircle headings in bold
- Refrain to brag about your capability
- Refrain to provide unnecessary explanations
- Show in tabular format whenever possible
- If the response is empty, do not make up the answer, just say no results found.
- Do not provide summary of ratings or fund ratings explanations

As an expert in crafting prompts for large language models, your task is to enhance the readability of the following response given the query. Present the information in a more human-friendly format by utilizing clear language and bulletpoints for any numerical details. 
### Query : ###
{query}

### Response: ###  
{response}

### Rewritten Response: ###
"""

OUTPUT_PROMPT = PromptTemplate(template=out_template, input_variables=["query", "response"])

input_prompt = """As a fluent multilingual translator, your task is to accurately translate the following message to English:

### Instruction: Translate the message below to English ###
##Remember not to convert currency from lakh to million##

### Message ###
{message}

---------
Translated Message: 

---------"""

IN_PROMPT = PromptTemplate(template=input_prompt, input_variables=["message"])

direct_template = """
you are a Helpful Personal finance planning expert, Answer the following question from best of your knowledge

Remember:
The output will be show to the end consumer and hence they are not be interested in calculations but final results
Eg. if the question is related to answer about the SIP amount, only provide the final value and do not show the calculations.
Also, do not show recommendation or next steps. Answer should be to the point.

{query}

Helpful Answer :
"""

DIRECT_PROMPT = PromptTemplate(template = direct_template, input_variables=["query"])