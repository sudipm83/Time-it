import altair as alt
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import streamlit_authenticator as stauth


# pip install streamlit-authenticator
# pip install streamlit-option_menu
# pip install langchain
# pip install python-dotenv

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


def show_nlp():
    st.write('this is nlp section')


def convert_pass():
    hashed_password = stauth.Hasher(['pass']).generate()
    return hashed_password
