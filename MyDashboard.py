import datetime

import streamlit as st
import plotly.express as px
import pandas as pd

from Util import show_my_nlp


def show_my_dashboard(loggedinusername):
    df = pd.read_csv('Employee data 2.csv')
    df = df[df["Employee Name"] == loggedinusername]
    df_original = df

    col1, col2 = st.columns(2)
    df["Swipein Date"] = pd.to_datetime(df["Swipein Date"])
    df["Swipeout Date"] = pd.to_datetime(df["Swipeout Date"])
    # Getting the min and max date
    startDate = pd.to_datetime(df["Swipein Date"]).min()
    endDate = pd.to_datetime(df["Swipein Date"]).max()

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))
        date2 = datetime.datetime.combine(date2, datetime.time(23, 59))
    # swipe in date shouldn't begreater than end date /// TO DO
    df = df[(df["Swipein Date"] >= date1) & (df["Swipein Date"] <= date2)].copy()

    st.subheader("Employee wise data")
    fig = px.bar(df, x="Swipein Date", y="Total hours",
                 text=['{:,.2f} hrs'.format(x) for x in df["Total hours"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

    if st.checkbox('show raw data', False):
        st.write(df_original)

    show_my_nlp(df_original)
    # download_csv(df_original)
