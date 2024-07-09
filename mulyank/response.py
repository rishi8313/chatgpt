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

sm_cap_alloc_cur_past_ot = PromptTemplate(
    template="""
System suggestion was {R} & {S}
""",
input_variables=["R","S"],
output_parser=None
)

sml_cap_alloc_ot = PromptTemplate(
    template="""
At current juncture : Allocation in Large cap should be {Q}%, Midcap should be {R}% , small cap should be {S}%.
""",
input_variables=["Q","R","S"],
output_parser=None)

equity_decision_ot = PromptTemplate(
    template="""
Broader inference for Limited action advisor is ( Looking for Entry & Exit ) to {F}.
Broader inference for Minimalistic action advisor is ( Looking for Entry but will never Sell ) to {H}
""",
input_variables=["F","H"],
output_parser=None
)

equity_debt_decision_ot = PromptTemplate(
    template="""Broader inference for Limited action advisor is ( Looking for Entry & Exit ) to {F}. 
    Broader inference for Minimalistic action advisor is ( Looking for Entry but will never Sell ) to {H}. 
    Invest {L}% of your Debt money in Long term Debt and {M}% of your debt money in Short term Debt.
""",
input_variables=["F","H","L","M"],
output_parser=None
)

market_fall_undervalue_ot = PromptTemplate(
    template="""We don’t believe in prediction. We help you prepare thorugh current assessment of score. If Valuation + Business cycle score are below 5.75, market has very limited downside in the absence of any six-sigma event. Along with that if Fine tuner ( Shiller + Buffet ) are green its a time to sell everything and BUY EQUITY.  
    Broader inference for Limited action advisor is ( Looking for Entry & Exit ) to {F}. Broader inference for Minimalistic action advisor is ( Looking for Entry but will never Sell ) to keep {H}.
    """,
input_variables=["F","H"],
output_parser=None
)

market_up_overvalue_ot = PromptTemplate(
    template="""We don’t believe in prediction. We help you prepare thorugh current assessment of score. If Valuation + Business cycle score are above 6. Along with that if Fine tuner ( Shiller + Buffet ) are Red its a time to start selling and underweight Equity.
    Broader inference for Limited action advisor is ( Looking for Entry & Exit ) to {F}. Broader inference for Minimalistic action advisor is ( Looking for Entry but will never Sell ) to keep {H}.
    """,
input_variables=["F","H"],
output_parser=None
)

current_market_value_ot = PromptTemplate(
    template=""" Market get Over-valued when inference is to Under-weight Equity and get Undervalued when broader inference is to Over-weight Equity and during Neutral Equity it becomes Fairly-valued. 
    Current scores for Valuation & Business cycle is {B} & {C} Respectively.  
    Broader inference for Limited action advisor is ( Looking for Entry & Exit ) to {F}. 
    Broader inference for Minimalistic action advisor is ( Looking for Entry but will never Sell ) to keep {H}.
    """,
input_variables=["B","C","F","H"],
output_parser=None
)

backtesting_broader_guidance_ot = PromptTemplate(
    template="""{G}""",
input_variables=["G"],
output_parser=None
)

debt_allocation_back_testing_ot = PromptTemplate(
    template="""{J}""",
input_variables=["J"],
output_parser=None
)

mid_small_cap_current_view_ot = PromptTemplate(
    template="""Current Score for Midcap is {O}. 
    Current Score for Smallcap is {P}. 
    0 means no action. 
    Below -50 means Go underweight in Mid and Small cap. 
    Above  50 means Go overweight in Mid & Small cap. 
    Eg : If I have 20 % Portfolio in MIDCAP And score is showing -50. Than allocation will be 10 % in Midcap. 
    If i have a portfolio of 20 % in Midcap and  If Midcap score is 100, than allocation will be 40 % in Micdap. 
    Similarly calculation for Small cap.  """,
input_variables=["O","P"],
output_parser=None
)

category_selection_under_debt_ot = PromptTemplate(
    template = """
 under Debt, one should invest in {N}
""",
input_variables=["N"]
)

category_selection_under_equity_ot = PromptTemplate(
    template = """
Currently under Equity, one should invest in {V}
""",
input_variables=["V"]
)

allocation_reco_no_investor_profile_ot = PromptTemplate(
    template="""
Out of 100 rs., One should keep {N} rs in Equity. This {N} rs should go in {V} now. Rest of the money should go in {W}. 
""",
input_variables=["N","V","W"]
)


OUTPUT_TEMPLATES = {
    "market_scenario": [market_scenario_ot, None],
    "capital_allocation": [capital_allocation_ot, None],
    "investment_advice" : [investment_advice_ot, None],
    "debt_market_view" : [debt_market_view_ot, None],
    "debt_allocation" : [debt_allocation_ot, None],
    "large_cap_allocation":[large_cap_allocation_ot,None],
    "small_mid_cap_allocation_current":[sm_cap_alloc_cur_ot,"add"],
    "small_mid_cap_allocation_past":[sm_cap_alloc_cur_past_ot,None],
    "small_mid_large_cap_allocation":[sml_cap_alloc_ot, None],
    "equity_decision":[equity_decision_ot,None],
    "equity_debt_decision":[equity_debt_decision_ot,None],
    "market_fall_undervalue":[market_fall_undervalue_ot,None],
    "market_up_overvalue":[market_up_overvalue_ot, None],
    "current_market_value":[current_market_value_ot,None],
    "backtesting_broader_guidance":[backtesting_broader_guidance_ot, None],
    "debt_allocation_back_testing":[debt_allocation_back_testing_ot,None],
    "mid_small_cap_current_view":[mid_small_cap_current_view_ot,None],
    "category_selection_under_debt":[category_selection_under_debt_ot, None],
    "category_selection_under_equity":[category_selection_under_equity_ot, None],
    "allocation_reco_no_investor_profile":[allocation_reco_no_investor_profile_ot,"frac"]
}
