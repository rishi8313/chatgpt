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
aggressive_investor_allocation_reco_ot = PromptTemplate(
    template="""Mention all the 3 points in table
1) Out of 100 rs For Aggressive All In investor, one should keep {A} Rs in Equity. 
2) Out of 100 rs For Aggressive All IN & All OUT investor, one should keep {B} Rs in Equity.
3) Out of 100 rs For Aggressive with Regular Re-balancing investor, one should keep {C} Rs in Equity.
Equity Money for Aggressive profile will go in {D}.
Debt Money should go in {E}.

Calculate following breakdown based on the amount mentioned in the question.
Large , Mid and Small cap allocation will be {F}, {G} , {H} respectively out of 100 rs in Equity.
    """, 
    input_variables=["A","B","C","D","E","F","G","H"]
    )

moderate_investor_allocation_reco_ot = PromptTemplate(
    template="""Out of 100 rs Moderate with Limited Rebalancing  & No Debt Category or looking for Capital Withdrawal investor, should keep {AE}. 
    Out of 100 Rs. For Moderate with regular rebalanacing investor , {AF} rs should go in Equity. 
    This Equity money should go in {N} now.
    Debt money should go in {V}.
    """, 
    input_variables=["AE","AF","N","V"]
    )
conservative_investor_allocation_reco_ot = PromptTemplate(
    template="""Out of 100 rs Moderate with Limited Rebalancing  & No Debt Category or looking for Capital Withdrawal investor, should keep in {AG}. 
    Conservative investor looking only for Debt category should go in {N}.
    """, 
    input_variables=["AG","N"]
    )
style_or_factor_sel_large_cap_ot = PromptTemplate(
    template="""
In large cap space, {AH} & {AI} are favourable factor.
    """, 
    input_variables=["AH","AI"]
    )
style_or_factor_sel_mid_cap_ot = PromptTemplate(
    template="""
In Mid cap space, {AK} & {AL} are favourable factor.
    """, 
    input_variables=["AK","AL"]
    )
style_or_factor_sel_small_cap_ot = PromptTemplate(
    template="""
In Small cap space, {AM} are favourable factor.
    """, 
    input_variables=["AM"]
    )

style_or_factor_all_3_ot = PromptTemplate(
    template="""
1) In Large , Mid . Small allocation will be {A} , {B} , {C} respectively .
2) In debt allocation should be {D}.
3) In large cap space, {E} & {F} are favourable factor.
4) In Mid cap space, {G} & {H} are favourable factor.
5) In Small cap space, {I} are favourable factor.
""",
input_variables=["A","B","C","D","E","F","G","H","I"]
)


performance_style_factor_selection_ot = PromptTemplate(
    template="""
In a large cap oriented style performance , {AJ}. 
In ALL CAP Oriented style performance , {AR}.
No one knows Financial market future performance. On 5 year Rolling basis, 99.9 % Probability that its Risk - adjusted performance would be better than most of the advisory Fraternity doing allocation across
    """, 
    input_variables=["AJ","AR"]
    )

debt_investment_0_1_ot = PromptTemplate(
    template="For very very short duration , your money upto 1 month should always go in {AS}",
    input_variables=["AS"]
)

debt_investment_1_3_ot = PromptTemplate(
    template="For Very short duration , your money upto 3 month should always go in {AT}",
    input_variables=["AT"]
)

debt_investment_3_6_ot = PromptTemplate(
    template="For Short duration , your money upto 6 month should go in {AU}",
    input_variables=["AU"]
)

debt_investment_6_18_ot = PromptTemplate(
    template="Your money upto 18 month should go in {AV}",
    input_variables=["AV"]
)

debt_investment_18_ot = PromptTemplate(
    template="Your money for than 18 month should go in {AW}",
    input_variables=["AW"]
)

SIP_1_6_ot = PromptTemplate(
    template="For every 1 Rs. SIP break-up. Your money sould go : {B} Rs. In Flexi Cap fund.   {C} Rs. In Multi Cap  FUND. {D} Rs. In BAF Fund. {E} Rs. In ESF Fund.",
    input_variables=["B","C","D","E"]
)

SIP_6_11_12_ot = PromptTemplate(
    template="For every 1 Rs. SIP break-up. Your money sould go : {B} Rs. In Flexi Cap fund.   {C} Rs. In Multi Cap  FUND. {D} Rs. In Mid Cap Fund. {E} Rs. In Small Cap Fund.",
    input_variables=["B","C","D","E"]
)

pe_pbv_scores_ot = PromptTemplate(
    template = "Current PE and PBV scores are {D} & {E} respectively. Broader Inference from the scores are if any of the Score is near 0 than :  Margin of Safety is Favourable in Equity as an Asset class. Probability of making money in coming 12 to 24 month is decent. If both the Scores are near or Below 0 than : Margin of safety is extremely Favourable. Accumulate Equity as an asset class from both hands.  If both the score are near 1  : Than more than half of the safety is gone and the view is Neutral on Equity as an Asset class.  If both the score are near or above 1.25 than : Have cautious stance on market. If Both are near or above 1.5 than : Exit Equity as asset class or Stop putting fresh money atleast. ",
    input_variables=["D","E"]
)

domestic_sectorial_ranking_ot = PromptTemplate(
    template = """Following are Sectors for tactical allocation / where one can put money - Rank , Sector Name , Relative Allocation.
    {A}
      OW means one can over-weight sector and priority can be given to Over-weight one.  NW means one can be Neutral-weight on the sector. UW means one can Under-weight sectors and should be avoided for tactical calls. """,
    input_variables=["A"]
)

style_factor_funds_ot = PromptTemplate(
    template = """Following are style/factor based fund along with first and second priority list. 
{A}
Priority with 1 are currently favourable funds and one should distribute money according to allocation suggested by MULYANKAN GPT.
""",
input_variables=["A"]
)

index_funds_ot = PromptTemplate(
    template = """Following are plain vanila index for portfolio creation.
{A}
 one should distribute money according to allocation suggested by MULYANKAN GPT FOR Large , Mid and small cap.
""",
input_variables=["A"]
)

sector_funds_ot = PromptTemplate(
    template = """Following are list of sectoral fund for tactical allocation. 
{A}
one should distribute money according to allocation suggested by MULYANKAN GPT FOR Sectoral ranking.
""",
input_variables=["A"]
)

past_tactical_calls_ot = PromptTemplate(
    template = """Some of the recent tactical call on Sectoral and global markets were : 
{A}
For more history of our bold call / Tactical alerts : Here is the link - https://mulyankangurukul.in/category/tactical-thematic/
""",
input_variables=["A"]
)


OUTPUT_TEMPLATES = {
    "market_scenario": [market_scenario_ot, "convert_to_perc"],
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
    "backtesting_broader_guidance_equity":[backtesting_broader_guidance_ot, "concat"],
    "debt_allocation_back_testing":[debt_allocation_back_testing_ot,"all"],
    "mid_small_cap_current_view":[mid_small_cap_current_view_ot,None],
    "category_selection_under_debt":[category_selection_under_debt_ot, None],
    "category_selection_under_equity":[category_selection_under_equity_ot, None],
    "allocation_reco_no_investor_profile":[allocation_reco_no_investor_profile_ot,"frac"],
    "aggressive_investor_allocation_reco": [aggressive_investor_allocation_reco_ot,"frac_aggr"],
    "moderate_investor_allocation_reco": [moderate_investor_allocation_reco_ot,"multiply_100"],
    "conservative_investor_allocation_reco": [conservative_investor_allocation_reco_ot,None],
    "style_or_factor_sel_large_cap": [style_or_factor_sel_large_cap_ot,None],
    "style_or_factor_sel_mid_cap": [style_or_factor_sel_mid_cap_ot, None],
    "style_or_factor_sel_small_cap": [style_or_factor_sel_small_cap_ot, None],
    "style_or_factor_all_3":[style_or_factor_all_3_ot, None],
    "performance_style_factor_selection": [performance_style_factor_selection_ot, "concat_perf"],
    "debt_investment_0_1":[debt_investment_0_1_ot,None],
    "debt_investment_1_3":[debt_investment_1_3_ot,None],
    "debt_investment_3_6":[debt_investment_3_6_ot,None],
    "debt_investment_6_18":[debt_investment_6_18_ot,None],
    "debt_investment_18+":[debt_investment_18_ot,None],
    "SIP_1_6" : [SIP_1_6_ot, "divide_by_10000"],
    "SIP_6_11" : [SIP_6_11_12_ot, "divide_by_10000"],
    "SIP_12+" : [SIP_6_11_12_ot, "divide_by_10000"],
    "pe_pbv_scores" : [pe_pbv_scores_ot, None],
    "domestic_sectorial_ranking" : [domestic_sectorial_ranking_ot, "all"],
    "style_factor_funds" : [style_factor_funds_ot, "all"],
    "index_funds" : [index_funds_ot, "all"],
    "sector_funds" : [sector_funds_ot, "all"],
    "past_tactical_calls" : [past_tactical_calls_ot, "all"]
}
