import datetime

import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
from PyPDF2 import PdfReader


def show_dashboard():
    df = pd.read_csv('Employee data 2.csv')

    clm1, clm2, clm3 = st.columns(3)

    with clm1:
        # Create for team
        team = st.multiselect("Pick your Team", df["Team Name"].unique())
        if not team:
            df2 = df.copy()
        else:
            df2 = df[df["Team Name"].isin(team)]

    with clm2:
        # Create for scrum team
        scrumTeam = st.multiselect("Pick the scrum team", df2["Scrum team name"].unique())
        if not scrumTeam:
            df3 = df2.copy()
        else:
            df3 = df2[df2["Scrum team name"].isin(scrumTeam)]

    with clm3:
        # Create for employee
        teamMember = st.multiselect("Pick team member", df3["Employee Name"].unique())

    col1, col2 = st.columns((2))
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

    df = df[(df["Swipein Date"] >= date1) & (df["Swipein Date"] <= date2)].copy()

    # Filter the data based on Region, State and City

    if not team and not scrumTeam and not teamMember:
        filtered_df = df
    elif not scrumTeam and not teamMember:
        filtered_df = df[df["Team Name"].isin(team)]
    elif not team and not teamMember:
        filtered_df = df[df["Scrum team name"].isin(scrumTeam)]
    elif scrumTeam and teamMember:
        filtered_df = df3[df["Scrum team name"].isin(scrumTeam) & df3["Employee Name"].isin(teamMember)]
    elif team and teamMember:
        filtered_df = df3[df["Team Name"].isin(team) & df3["Employee Name"].isin(teamMember)]
    elif team and scrumTeam:
        filtered_df = df3[df["Team Name"].isin(team) & df3["Scrum team name"].isin(scrumTeam)]
    elif teamMember:
        filtered_df = df3[df3["Employee Name"].isin(teamMember)]
    else:
        filtered_df = df3[
            df3["Team Name"].isin(team) & df3["Scrum team name"].isin(scrumTeam) & df3["Employee Name"].isin(
                teamMember)]

    emp_df_sum = filtered_df.groupby(by=["Employee Name"], as_index=False)["Total hours"].sum()
    emp_df_avg = filtered_df.groupby(by=["Team Name"], as_index=False)["Total hours"].mean()

    with col1:
        st.subheader("Employe wise data")
        fig = px.bar(emp_df_sum, x="Employee Name", y="Total hours",
                     text=['{:,.2f} hrs'.format(x) for x in emp_df_sum["Total hours"]],
                     template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)

    with col2:
        st.subheader("Team wise data")
        fig = px.pie(emp_df_avg, values="Total hours", names="Team Name")
        fig.update_traces(text=filtered_df["Team Name"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    if st.checkbox('show raw data', True):
        st.write(filtered_df)
