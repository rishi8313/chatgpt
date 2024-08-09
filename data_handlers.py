import os
from sqlalchemy import create_engine
from sqlalchemy import text

def handle_fact_sheet(data):
    data.columns = data.columns.str.strip()
    columns = list(data.columns)
    columns[5] = "Advisory guidance for entry and exit zones"
    columns[7] = "Equity entry guidance with stop-loss strategy"
    columns[30] = "Balanced Withdrawal Strategy"
    columns[32] = "Conservative Withdrawal Approach"
    data.columns = columns
    data = data.round(3)
    return data, "fact_sheet"
    
def handle_time_goal_based(data):
    data.columns = data.columns.str.strip()
    data.dropna(axis = 1, inplace = True)
    return data, "time_goal_based"


def handle_pe_pbv_scores(data):
    data.columns = data.columns.str.strip()
    data = data.ffill()
    data["Year"] = data["Year"].apply(lambda x : int(x))
    return data, "pe_pbv_simple_scores"

def handle_fund_filteration_equity(data):
    data.columns = data.columns.str.strip()
    return data, "fund_filteration_equity"

def handle_fund_filteration_hybrid(data):
    data.columns = data.columns.str.strip()
    return data, "fund_filteration_hybrid"

def handle_fund_filteration_debt(data):
    data.columns = data.columns.str.strip()
    return data, "fund_filteration_debt"


def handle_domestic_sectorial_ranking(data):
    data.columns = data.columns.str.strip()
    return data, "domestic_sectorial_ranking"

def handle_style_factor_funds(data):
    data.columns = data.columns.str.strip()
    return data, "style_factor_funds"

def handle_index_funds(data):
    data.columns = data.columns.str.strip()
    return data, "index_funds"

def handle_sector_funds(data):
    data.columns = data.columns.str.strip()
    return data, "sector_funds"

def handle_global_funds(data):
    data.columns = data.columns.str.strip()
    return data, "global_funds"

def handle_past_tactical_calls(data):
    data = data.dropna()
    data.columns = data.columns.str.strip()
    return data, "past_tactical_calls"
