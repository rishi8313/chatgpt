import streamlit as st
import numpy as np

import pandas as pd
import os
from dotenv import load_dotenv

from data_handlers import *

if not load_dotenv("/etc/secrets/.env"):
    load_dotenv("mulyank/etc/secrets/.env")

sheet_to_function_mapping = {
    "Data Source":handle_fact_sheet,
    "Time & Goal Based":handle_time_goal_based,
    "PE PBV SIMPLE SCORES":handle_pe_pbv_scores,
    "Fund Filtration Equity":handle_fund_filteration_equity,
    "Fund Filtration Hybrid" : handle_fund_filteration_hybrid,
    "Fund Filtration Debt" : handle_fund_filteration_debt,
    "Domestic Sectoral Ranking" : handle_domestic_sectorial_ranking,
    "Style Factor Funds" : handle_style_factor_funds,
    "Index Funds": handle_index_funds,
    "Sector Funds": handle_sector_funds,
    "Global Funds": handle_global_funds,
    "Past Tactical Calls" : handle_past_tactical_calls,

}

def update(data, table_name):
    db_connection_str = os.environ["DB_CONNECTION_STR"]
    db_connection = create_engine(db_connection_str)

    engine = create_engine(db_connection_str)
    with engine.connect() as conn:
        try:
            conn.execute(text("DROP TABLE {}".format(table_name)))
        except:
            pass
        data.to_sql(name = table_name, con = db_connection)

def show_and_update(data, table_name):
    st.write(data)
    if st.button("Update"):
        update(data, table_name)
        st.write("Data updated in {}".format(table_name))

def show_and_update_all(data, table_names):
    tabs = st.tabs(table_names)
    print(table_names)
    for d, tab, table_name in zip(data, tabs,table_names):
        with tab:
            st.header(table_name)
            st.write(d)
    if st.button("Update"):
        with st.spinner("Updating the database"):
            for d, table_name in zip(data, table_names):
                update(d, table_name)
            st.write("Data updated in all tables")

def main():
    st.set_page_config(initial_sidebar_state='expanded', page_title='Mulyankan GPT', page_icon=":moneybag:", layout="wide")
    cols = st.sidebar.columns([0.4,0.6])
    with cols[0]:
        st.image("icons/Mulyankan_Icon.jpeg", width=100)
    with cols[1]:
        ## Define sidebar
        st.title("**Mulyankan/मुल्यांकन GPT**")
    st.sidebar.markdown("<h5 style='font-size: 12px;'>Allocate , Rebalance , Review -  Powered by AI for MFD/RIA/WEALTH MANAGERS</h5>", unsafe_allow_html=True)
    for i in range(14):
        st.sidebar.write("")

    st.sidebar.title("_Disclaimer_")
    st.sidebar.markdown("""<h5 style='font-size: 10px;'>Note: Our services/platform/website are meant for Professional financial intermediaries only. The information and content offered in this subscription are intended for
educational purposes only. We don’t provide personalized investment advice. We don’t provide Fund selection and Security/Stock selection advice or any trading strategy. The content on this website, including articles, blog posts, educational
materials, and any other communications, is copyrighted by Mulyankan
Gurukul. Copying, Duplication or sharing of our subscription content
with unauthorized users will result in the immediate
termination of your subscription. We are not liable for any losses or damages, directly or
indirectly, arising from the use or inability to use this
subscription's content.</h5>""", unsafe_allow_html=True)
    
    if file := st.file_uploader("Upload the latest data"):
        option = st.selectbox("Select Sheet to update",["Update All"] + pd.ExcelFile(file).sheet_names)
        if option == "Update All":
            cleaned_data, table_names = [], []
            for sheet_name in sheet_to_function_mapping.keys():
                data = pd.read_excel(file, sheet_name=sheet_name)
                if sheet_name in sheet_to_function_mapping.keys():
                    clean_data, table_name = sheet_to_function_mapping[sheet_name](data)
                    cleaned_data.append(clean_data)
                    table_names.append(table_name)
            show_and_update_all(cleaned_data, table_names)
        else:
            sheet_name = option
            data = pd.read_excel(file, sheet_name=sheet_name)
            if sheet_name in sheet_to_function_mapping:
                data, table_name = sheet_to_function_mapping[sheet_name](data)
                show_and_update(data, table_name)

if __name__ == "__main__":
    main()