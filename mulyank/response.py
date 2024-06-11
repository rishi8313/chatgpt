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

debt_market_view_ot = PromptTemplate(
    template="""
Current Debt score is {I}. One should go in {K}
""",
    input_variables=["I","K"],
output_parser = None)

debt_allocation_ot = PromptTemplate(
    template="""
Invest {L}% of your Debt money in Long term Debt and {M}% of your debt money in Short term Debt.
""",
    input_variables=["L","M"],
output_parser = None)

large_cap_allocation_ot = PromptTemplate(
    template="""
At current juncture : Allocation in Large cap should be {Q} %.
""",
input_variables=["Q"],
output_parser=None)

sm_cap_alloc_cur_ot = PromptTemplate(
    template="""
At current juncture : Allocation in MID & SMALL CAP  should be {R + S} %.
""",
input_variables=["R","S"],
output_parser=None
)

sm_cap_alloc_cur_past = PromptTemplate(
    template="""
System suggestion was {R} & {S}
""",
input_variables=["R","S"],
output_parser=None
)

equity_decision_out = PromptTemplate(
    template="""
Broader inference for Limited action advisor is ( Looking for Entry & Exit ) to {F}.
Broader inference for Minimalistic action advisor is ( Looking for Entry but will never Sell ) to {H}
""",
input_variables=["F","H"],
output_parser=None
)

OUTPUT_TEMPLATES = {
    "market_scenario": [market_scenario_ot, None],
    "capital_allocation": [capital_allocation_ot, None],
    "investment_advice" : [investment_advice_ot, None],
    "debt_market_view" : [debt_market_view_ot, None],
    "debt_allocation" : [debt_allocation_ot, None],
    "large_cap_allocation":[large_cap_allocation_ot,None],
    "small_mid_cap_allocation_current":[sm_cap_alloc_cur_ot,"add"],
    "small_mid_cap_allocation_past":[sm_cap_alloc_cur_past,None],
    "equity_decision":[equity_decision_out,None]
}
