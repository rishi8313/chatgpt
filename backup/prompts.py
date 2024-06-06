from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains.router.llm_router import RouterOutputParser

PROMPT_PREFIX = """Answer the following question

{question}

by providing the following information, if timeframe is not mentioned use the latest date present in database:
"""

market_scenario_prompt_template = PROMPT_PREFIX + """
Get "Valuation Distilled Score", "Blended Distilled Score","Shiller score",
"buffet score","Broader Guidance - Inference for Limited Action Advisor looking for both :-  Favourable zone to enter and Unfavourable Zone to exit",
"Broader Guidance - Inference for Minimalistic Action Advisor looking for ONLY :-  Favourable zone to enter Equity and will run STP in Un-favourable zone"
from fact_sheet
"""

capital_allocation_prompt_template = PROMPT_PREFIX + """
Get "Broader Guidance - Inference for Limited Action Advisor looking for both :-  Favourable zone to enter and Unfavourable Zone to exit",
"Broader Guidance - Inference for Minimalistic Action Advisor looking for ONLY :-  Favourable zone to enter Equity and will run STP in Un-favourable zone"
from fact_sheet
"""

investment_advice_prompt_template = PROMPT_PREFIX + """
Get value of 'Broader Guidance - Inference for Minimalistic Action Advisor looking for ONLY :-  Favourable zone to enter Equity and will run STP in Un-favourable zone'
from fact_sheet
"""

def get_prompt(template):
    return PromptTemplate(
    template=template,
    input_variables=["question"],
    output_parser=None
)

greetings_out = "Hi..!! I am Mulyankan GPT. How may I help you today?"

mulyank_working_out = "Studying Band theory of Valuation based on Past data does not work. Our system further calculate derived values of 20 + time-tested metric through lens of data science. Mulyankan GPT deeply study Valuation and Business cycle through Structured framework and advanced algorithm. It gives guidance on the basis of Where we are Standing in the Cycle/Zone."

event_handling_out = "Mulyankan GPT doesnot base its guidance on news, event analysis or by studying absolute level of indices like Sensex or NIFTY."

future_question_out = "Mulyankan GPT doesnot base its guidance on news, event analysis or by studying absolute level of indices like Sensex or NIFTY."

market_scenario_prompt = get_prompt(market_scenario_prompt_template)

capital_allocation_prompt = get_prompt(capital_allocation_prompt_template)

investment_advice_prompt = get_prompt(investment_advice_prompt_template)

prompt_infos = [
    {'name':'greetings',
     'description':'Basic greetings from user, eg. Hi, Hello etc.'},
    {'name':'mulyankan_working',
     'description':'Basic working of mulyankan gpt, eg. how mulyankan gpt works?'},
    {'name':'event_handling',
     'description': 'Effect of events, eg. According to you, how will the global warming impact the stocks, What do you think of XYZ event?/What is your election prediction?'},
    {'name':'future_question',  
     'description' : "Answers any question asked in future tense or asking for a prediction, eg. how market will behave, How will global warming impact?"},
    {'name':'market_scenario',
     'description': 'Answers question regarding current market outlook/scenario, equity market, current equity scores in a year and broader inference from scores'},
    {'name':'capital_allocation', 
     'description' : 'Asset Allocation Details. Ex. What should be my capital allocation / Broader Asset allocation based on Current market ?'},
    {'name':'investment_advice_prompt_template',
     'description' : 'Investment Advice. Ex. Do I go for lumsum or Staggered investment/stp at current juncture ? when the system has last told to STOP STP and go into Equity ?'}
]

query_mapping = {"greetings" : greetings_out,
                 "mulyankan_working" : mulyank_working_out,
                 "event_handling" : event_handling_out,
                 "future_question" : future_question_out,
                 "market_scenario": market_scenario_prompt,
                 "capital_allocation": capital_allocation_prompt,
                 "investment_advice_prompt_template" : investment_advice_prompt}

destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
destinations_str = "\n".join(destinations)

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
    destinations=destinations_str
)

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)