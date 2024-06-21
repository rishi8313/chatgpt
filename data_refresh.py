import streamlit as st
import numpy as np
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

if not load_dotenv("/etc/secrets/.env"):
    load_dotenv("mulyank/etc/secrets/.env")

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
        data = pd.read_excel(file)
        data.columns = data.columns.str.strip()
        columns = list(data.columns)
        columns[5] = "Advisory guidance for entry and exit zones"
        columns[7] = "Equity entry guidance with stop-loss strategy"
        columns[-14] = "Balanced Withdrawal Strategy"
        columns[-12] = "Conservative Withdrawal Approach"
        data.columns = columns
        data = data.round(3)
        st.write(data)
        if st.button("Update"):
            db_connection_str = os.environ["DB_CONNECTION_STR"]
            db_connection = create_engine(db_connection_str)
            db_connection.execute("DROP TABLE fact_sheet")
            with st.spinner("Updating"):
                data.to_sql(name = "fact_sheet", con = db_connection)
            st.write("Data updated in Database")

if __name__ == "__main__":
    main()