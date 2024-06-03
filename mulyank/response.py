from langchain.prompts import PromptTemplate

market_scenario_ot = PromptTemplate(
    template="""
Valuation cycle distiled score is {B}. Score varies from 4 to 8. It tells us where are we standing 
in Valuation cycle. Refer Valuatio cycle algo for in-depth exploration. It is a Unified score for 
all Valuation cycle metrics.  Business Cycle distilled score {C}. Score varies from 4 to 8. 
It tells us where are we standing in Earning cycle. Refer Business cycle algo for in-depth exploration 
Fine Tuner Shiller is {D}% .Fine Tuner Buffet is {E}%. Buffet got activated  
as Strong sell zone. Fine tuner as a whole got activated as STRONG SELL when both are above 
threshold i.e Shiller above 150% and Buffet above 135%. Fine tuner as a whole got activated as 
STRONG BUY when both are below threshold i.e Shiller BELOW 85% and Buffet BELOW 85%. Equity markets 
are Favourable when both Valuation + Business distilled score is below 5.75 and extremely favourable 
when any one of them near 5.  Broader inference for Limited action advisor is ( Looking for Entry & Exit ) 
to {F}. Broader inference for Minimalistic action advisor is ( Looking for Entry 
but will never Sell ) to keep {H}.
""",
    input_variables=["B","C","D","E","F","H"],
    output_parser=None)

capital_allocation_ot = PromptTemplate(
    template="""
Broader inference for Limited action advisor is ( Looking for Entry & Exit ) to {F}. 
Broader inference for Minimalistic action advisor is ( Looking for Entry but will never Sell ) to keep 
{H}
""",
    input_variables=["F","H"],
    output_parser=None) 

investment_advice_ot = PromptTemplate(
    template="""
System will tell you according to Cycle/Zone when to start STP and when to STOP. 
Currently it is to keep {H}. 
""",
    input_variables=["H"],
    output_parser=None)


OUTPUT_TEMPLATES = {
    "market_scenario": market_scenario_ot,
    "capital_allocation": capital_allocation_ot,
    "investment_advice_prompt_template" : investment_advice_ot
}
