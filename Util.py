import altair as alt
import streamlit as st
# from langchain.agents import create_csv_agent
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import OpenAI
import pandas as pd
from dotenv import load_dotenv
import streamlit_authenticator as stauth


# pip install streamlit-authenticator
# pip install streamlit-option_menu
# pip install langchain
# pip install python-dotenv
# pip install langchain-experimental
# pip install openai

# streamlit run main.py

def show_graph():
    data = pd.read_csv("Employee login data 2.csv")
    chart = alt.Chart(data, title="login data").mark_bar(opacity=1).encode(
        column=alt.Column('date:0', spacing=3, header=alt.Header(labelOrient='bottom')),
        x=alt.X('Employee Name', sort=['ascending'], axix=None),
        y=alt.Y('total hours:Q'),
        color=alt.Color('Employee Name')
    ).configure_view(stroke='transparent')
    st.altair_chart(chart)


# def change_key(id)

def show_my_nlp(df_original):
    my_nlp = st.text_input("Enter your query !")
    # st.subheader(input_query)
    df_original.to_csv('LoggedInUser.csv', index=False)
    smart_chat('LoggedInUser.csv', my_nlp)


def show_employee_nlp(df_original):
    emp_nlp = st.text_input("Enter your query !")
    df_original.to_csv('LoggedInUser.csv', index=False)
    smart_chat('LoggedInUser.csv', emp_nlp)


def smart_chat(user_csv, question):
    load_dotenv()
    if user_csv is not None:
        user_question = question

        llm = OpenAI(temperature=0)
        agent = create_csv_agent(llm, user_csv, verbose=True)

        if user_question is not None and user_question != "":
            response = agent.run(user_question)

            st.write(response)


def download_csv(df_original):
    kuchTo = str()
    # pandas.DataFrame.to_csv
    # st.write(pd.read_csv(df_original.to_csv('LoggedInUser.csv', index=False)))


def smart_chat2(user_csv, question):
    st.write(user_csv + question)
    df = pd.read_csv(user_csv)
    st.write(df)


def convert_pass():
    hashed_password = stauth.Hasher(['pass']).generate()
    return hashed_password
