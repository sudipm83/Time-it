import datetime

import streamlit as st
import plotly.express as px
import pandas as pd

from Util import show_employee_nlp


def show_team_dashboard(name):
    df = pd.read_csv('Employe_data_refine_4.csv')

    clm1, clm2, clm3 = st.columns(3)
    df_l1 = df[df["manager_level_1"] == name]
    df_l2 = df[df["manager_level_2"] == name]
    df = pd.concat([df_l1, df_l2])
    df_original = df

    with clm1:
        # Create for team
        team = st.multiselect("Pick your Team", df["team_name"].unique())
        if not team:
            df2 = df.copy()
        else:
            df2 = df[df["team_name"].isin(team)]

    with clm2:
        # Create for scrum team
        scrumTeam = st.multiselect("Pick the scrum team", df2["scrum_team_name"].unique())
        if not scrumTeam:
            df3 = df2.copy()
        else:
            df3 = df2[df2["scrum_team_name"].isin(scrumTeam)]

    with clm3:
        # Create for employee
        teamMember = st.multiselect("Pick team member", df3["employee_name"].unique())

    col1, col2 = st.columns((2))
    df["swipe_date"] = pd.to_datetime(df["swipe_date"])
    # Getting the min and max date
    startDate = pd.to_datetime(df["swipe_date"]).min()
    endDate = pd.to_datetime(df["swipe_date"]).max()

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
        date1 = datetime.datetime.combine(date1, datetime.time(00, 00))
    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))
        date2 = datetime.datetime.combine(date2, datetime.time(23, 59))
    # swipe in date shouldn't begreater than end date /// TO DO
    df = df[(df["swipe_date"] >= date1) & (df["swipe_date"] <= date2)].copy()
    if date1 > date2:
        st.error('end date must be greater than start date')
    else:
        # Filter the data based on Region, State and City
        if not team and not scrumTeam and not teamMember:
            filtered_df = df
        elif not scrumTeam and not teamMember:
            filtered_df = df[df["team_name"].isin(team)]
        elif not team and not teamMember:
            filtered_df = df[df["scrum_team_name"].isin(scrumTeam)]
        elif scrumTeam and teamMember:
            filtered_df = df3[df["scrum_team_name"].isin(scrumTeam) & df3["employee_name"].isin(teamMember)]
        elif team and teamMember:
            filtered_df = df3[df["team_name"].isin(team) & df3["employee_name"].isin(teamMember)]
        elif team and scrumTeam:
            filtered_df = df3[df["team_name"].isin(team) & df3["scrum_team_name"].isin(scrumTeam)]
        elif teamMember:
            filtered_df = df3[df3["employee_name"].isin(teamMember)]
        else:
            filtered_df = df3[
                df3["team_name"].isin(team) & df3["scrum_team_name"].isin(scrumTeam) & df3["employee_name"].isin(
                    teamMember)]

        emp_df_sum = filtered_df.groupby(by=["employee_name"], as_index=False)["total_hours in hh:mm:ss"].sum()
        emp_df_avg = filtered_df.groupby(by=["scrum_team_name"], as_index=False)["total_hours in hh:mm:ss"].mean()
        with col1:
            st.subheader("Employee wise data")
            fig = px.bar(emp_df_sum, x="employee_name", y="total_hours in hh:mm:ss",
                         text=['{:,.2f} hrs'.format(x) for x in emp_df_sum["total_hours in hh:mm:ss"]],
                         template="seaborn")
            st.plotly_chart(fig, use_container_width=True, height=200)

        with col2:
            st.subheader("Team wise data")
            fig = px.pie(emp_df_avg, values="total_hours in hh:mm:ss", names="scrum_team_name")
            fig.update_traces(text=filtered_df["scrum_team_name"], textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

        if st.checkbox('show raw data', False):
            st.write(df_original)

        show_employee_nlp(df_original)
