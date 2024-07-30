import streamlit as st
import numpy as np
from mulyank.utils import generate_response
import copy



def main():
    
    st.set_page_config(initial_sidebar_state='expanded', page_title='Mulyankan GPT', page_icon=":moneybag:", layout="wide")
    st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True)
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
    
    cols = st.columns([0.9,0.1])
    st.markdown("<h5 style='font-size: 16px;'>Say good - bye to educated guesses and Gut/Narrative based decision and take Framework oriented : Guidance & System Driven : Action.</h5>", unsafe_allow_html=True)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    avatar = {"user": "icons/user.webp",
            "assistant" : "icons/bot.webp"}

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=avatar[message["role"]]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is the market condition today?", key="chat"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=avatar["user"]):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=avatar["assistant"]):
            with st.spinner("Analyzing"):
                stream = generate_response(st.session_state)
                response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    if st.button("Clear Chat"):
        st.session_state['messages'] = []
        st.rerun() 

if __name__ == "__main__":
    main()