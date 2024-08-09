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
        sheet_name = st.selectbox("Select Sheet to update", pd.ExcelFile(file).sheet_names)
        print(sheet_name)
        data = pd.read_excel(file, sheet_name=sheet_name)
        
        if sheet_name in sheet_to_function_mapping:
            sheet_to_function_mapping[sheet_name](st, data)
        # if sheet_name == "Data Source":
        #     handle_fact_sheet(st, data)
        # elif sheet_name == "Time & Goal Based":
        #     handle_time_goal_based(st, data)
        # elif sheet_name == "PE PBV SIMPLE SCORES":
        

if __name__ == "__main__":
    main()