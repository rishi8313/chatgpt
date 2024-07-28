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
            else:
                self.query_mapping[name] = self.handle_prompt_helper(name)

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
- Clearly present any numerical or factual information in bulletpoints
- seperate the facts by next line character ("\n")
- encircle headings in bold
- Refrain to brag about your capability
- Refrain to provide unnecessary explanations

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

### Message ###
{message}

---------
Translated Message: 

---------"""

IN_PROMPT = PromptTemplate(template=input_prompt, input_variables=["message"])