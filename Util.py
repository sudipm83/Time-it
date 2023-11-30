import altair as alt
import streamlit as st
# from langchain.agents import create_csv_agent
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import OpenAI
import pandas as pd
from dotenv import load_dotenv
import os
import streamlit_authenticator as stauth
import ctypes

# pip install streamlit-authenticator
# pip install streamlit-option_menu
# pip install langchain
# pip install python-dotenv
# pip install langchain-experimental
# pip install openai

# streamlit run main.py

counter = 0
submit_flag = False
query = ''


def show_graph():
    data = pd.read_csv("Employee login data 2.csv")
    chart = alt.Chart(data, title="login data").mark_bar(opacity=1).encode(
        column=alt.Column('date:0', spacing=3, header=alt.Header(labelOrient='bottom')),
        x=alt.X('Employee Name', sort=['ascending'], axix=None),
        y=alt.Y('total hours:Q'),
        color=alt.Color('Employee Name')
    ).configure_view(stroke='transparent')
    st.altair_chart(chart)


def toggle_flag():
    global submit_flag
    submit_flag = True
    st.write("toggled")
    # ctypes.windll.user32.MessageBoxW(0, "Your text", "Your title", 1)


def show_my_nlp(df_original):
    global submit_flag
    my_nlp = st.text_input("Enter your query !")
    # st.button("Submit my query")
    df_original.to_csv('my_nlp.csv', index=False)
    smart_chat('my_nlp.csv', my_nlp)


def show_employee_nlp(df_original):
    global submit_flag
    emp_nlp = st.text_input("Enter your query !")
    # st.button("Submit Emp query")
    df_original.to_csv('emp_nlp.csv', index=False)
    smart_chat('emp_nlp.csv', emp_nlp)


def smart_chat(user_csv, question):
    load_dotenv()
    global counter
    global submit_flag
    global query
    # st.write(submit_flag)
    submit_flag = False

    if question != query:
        query = question
        if counter < 2:
            counter = counter + 1
        else:
            counter = 1
        st.write('key used :'+str(counter))
        open_ai_key = os.environ.get("OPENAI_API_KEY_" + str(counter))
        if user_csv is not None:
            user_question = question
            llm = OpenAI(temperature=0, openai_api_key=open_ai_key)
            agent = create_csv_agent(llm, user_csv, verbose=True)
            if user_question is not None and user_question != "":
                response = agent.run(user_question)
                st.write(response)


def download_csv(df_original):
    kuchTo = str()
    # pandas.DataFrame.to_csv


def smart_chat2(user_csv, question):
    st.write(user_csv + ' ' + question)
    # df = pd.read_csv(user_csv)
    # st.write(df)


def convert_pass():
    hashed_password = stauth.Hasher(['pass']).generate()
    return hashed_password
