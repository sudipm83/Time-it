import datetime

import streamlit as st
import plotly.express as px
import pandas as pd

from Util import download_csv, show_my_nlp


def show_my_dashboard(loggedinusername):
    df = pd.read_csv('Employe_data_refine_4.csv')
    df = df[df["employee_name"] == loggedinusername]
    df_original = df

    col1, col2 = st.columns(2)
    #df["swipe_date"] = df["swipe_date"]
    df["swipe_date"] = pd.to_datetime(df["swipe_date"])
    # df["Swipeout Date"] = pd.to_datetime(df["Swipeout Date"])
    # Getting the min and max date
    startDate = pd.to_datetime(df["swipe_date"]).min()
    endDate = pd.to_datetime(df["swipe_date"]).max()

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))
        date2 = datetime.datetime.combine(date2, datetime.time(23, 59))
    # swipe in date shouldn't begreater than end date /// TO DO
    if date1 > date2:
        st.error('end date must be greater than start date')
    else :
        df = df[(df["swipe_date"] >= date1) & (df["swipe_date"] <= date2)].copy()

        st.subheader("Employee wise data")
        fig = px.bar(df, x="swipe_date", y="total_hours in hh:mm:ss",
                     text=['{:,.2f} hrs'.format(x) for x in df["total_hours in hh:mm:ss"]],
                     template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)

        if st.checkbox('show raw data', False):
            st.write(df_original)
        show_my_nlp(df_original)
        # download_csv(df_original)
