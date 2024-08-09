import os
from sqlalchemy import create_engine
from sqlalchemy import text

def show_and_update(st, data, table_name):
    st.write(data)
    if st.button("Update"):
        db_connection_str = os.environ["DB_CONNECTION_STR"]
        db_connection = create_engine(db_connection_str)

        engine = create_engine(db_connection_str)
        with engine.connect() as conn:
            try:
                conn.execute(text("DROP TABLE {}".format(table_name)))
            except:
                pass
            with st.spinner("Updating"):
                data.to_sql(name = table_name, con = db_connection)
            st.write("Data updated in {}".format(table_name))


def handle_fact_sheet(st, data):
    data.columns = data.columns.str.strip()
    columns = list(data.columns)
    columns[5] = "Advisory guidance for entry and exit zones"
    columns[7] = "Equity entry guidance with stop-loss strategy"
    columns[30] = "Balanced Withdrawal Strategy"
    columns[32] = "Conservative Withdrawal Approach"
    data.columns = columns
    data = data.round(3)
    show_and_update(st, data, "fact_sheet")

def handle_time_goal_based(st, data):
    data.columns = data.columns.str.strip()
    data.dropna(axis = 1, inplace = True)
    show_and_update(st, data, "time_goal_based")


def handle_pe_pbv_scores(st, data):
    data.columns = data.columns.str.strip()
    data = data.ffill()
    data["Year"] = data["Year"].apply(lambda x : int(x))
    show_and_update(st, data, "pe_pbv_simple_scores")

def handle_fund_filteration_equity(st, data):
    data.columns = data.columns.str.strip()
    show_and_update(st, data, "fund_filteration_equity")

def handle_fund_filteration_hybrid(st, data):
    data.columns = data.columns.str.strip()
    show_and_update(st, data, "fund_filteration_hybrid")

def handle_fund_filteration_debt(st, data):
    data.columns = data.columns.str.strip()
    show_and_update(st, data, "fund_filteration_debt")


def handle_domestic_sectorial_ranking(st, data):
    data.columns = data.columns.str.strip()
    show_and_update(st, data, "domestic_sectorial_ranking")

def handle_style_factor_funds(st, data):
    data.columns = data.columns.str.strip()
    show_and_update(st, data, "style_factor_funds")

def handle_index_funds(st, data):
    data.columns = data.columns.str.strip()
    show_and_update(st, data, "index_funds")

def handle_sector_funds(st, data):
    data.columns = data.columns.str.strip()
    show_and_update(st, data, "sector_funds")

def handle_global_funds(st, data):
    data.columns = data.columns.str.strip()
    show_and_update(st, data, "global_funds")

def handle_past_tactical_calls(st, data):
    data = data.dropna()
    data.columns = data.columns.str.strip()
    show_and_update(st, data, "past_tactical_calls")
