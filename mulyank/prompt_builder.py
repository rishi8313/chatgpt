from json import JSONDecoder
from langchain.prompts import PromptTemplate
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains.router.llm_router import RouterOutputParser

PROMPT_PREFIX = """Answer the following question

{question}

While creating the sql query, remember the following points
Remember : Always convert date provided in the question to datetime sql type while generating sql query.
Remember : Always use strftime date time matching for dates.
Remember : If date, month or year is not mentioned in the question, use the latest date present in database convert it to strftime format to match
Remember : If only month and year is mentioned, then take an Mean of whole month for the given year and provide the value
Remember : If only year is mentioned, then take an average of whole year and provide the value
Remember : If data, month and year all 3 are mentioned, then get the value for the exact date from the date column which is a datetime type column
Remember : To round off the values upto 2 decimal points only.
by providing the following information.

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
        prefix = "Get value of"
        columns_str = ",".join(columns)
        mid_sec = " from "
        template = PROMPT_PREFIX + "\n" + prefix + columns_str + mid_sec + table_name
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