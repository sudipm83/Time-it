import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
from PyPDF2 import PdfReader

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Time-it", page_icon=":bar_chart:", layout="wide")

st.title(" :chart_with_upwards_trend: Sample swipe-in data")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
def main():
    fl = st.file_uploader("Upload your file here", type=(["csv","txt","xlsx","xls","pdf"]))

    if fl is not None:
        filename = fl.name
        st.write(filename)
        # Reading from csv file
        if filename.__contains__('csv'):
            df = pd.read_csv(filename, encoding = "ISO-8859-1")
            col1, col2 = st.columns((2))
            df["Swipein Date"] = pd.to_datetime(df["Swipein Date"])

            # Getting the min and max date
            startDate = pd.to_datetime(df["Swipein Date"]).min()
            endDate = pd.to_datetime(df["Swipein Date"]).max()

            with col1:
                date1 = pd.to_datetime(st.date_input("Start Date", startDate))

            with col2:
                date2 = pd.to_datetime(st.date_input("End Date", endDate))

            df = df[(df["Swipein Date"] >= date1) & (df["Swipein Date"] <= date2)].copy()

            st.sidebar.header("Choose your filer :")

            # Create for team
            team = st.sidebar.multiselect("Pick your Team", df["Team Name"].unique())
            if not team:
                df2 = df.copy()
            else:
                df2 = df[df["Team Name"].isin(team)]

            # Create for scrum team
            scrumTeam = st.sidebar.multiselect("Pick the scrum team", df2["Scrum team name"].unique())
            if not scrumTeam:
                df3 = df2.copy()
            else:
                df3 = df2[df2["Scrum team name"].isin(scrumTeam)]

            # Create for employee
            teamMember = st.sidebar.multiselect("Pick team member", df3["Emp Name"].unique())

            # Filter the data based on Region, State and City

            if not team and not scrumTeam and not teamMember:
                filtered_df = df
            elif not scrumTeam and not teamMember:
                filtered_df = df[df["Team Name"].isin(team)]
            elif not team and not teamMember:
                filtered_df = df[df["Scrum team name"].isin(scrumTeam)]
            elif scrumTeam and teamMember:
                filtered_df = df3[df["Scrum team name"].isin(scrumTeam) & df3["Emp Name"].isin(teamMember)]
            elif team and teamMember:
                filtered_df = df3[df["Team Name"].isin(team) & df3["Emp Name"].isin(teamMember)]
            elif team and scrumTeam:
                filtered_df = df3[df["Team Name"].isin(team) & df3["Scrum team name"].isin(scrumTeam)]
            elif teamMember:
                filtered_df = df3[df3["Emp Name"].isin(teamMember)]
            else:
                filtered_df = df3[df3["Team Name"].isin(team) & df3["Scrum team name"].isin(scrumTeam) & df3["Emp Name"].isin(teamMember)]

            emp_df_sum = filtered_df.groupby(by=["Emp Name"], as_index=False)["Total hours"].sum()
            emp_df_avg = filtered_df.groupby(by=["Team Name"], as_index=False)["Total hours"].mean()



            with col1:
                st.subheader("Employe wise data")
                fig = px.bar(emp_df_sum, x="Emp Name", y="Total hours",
                             text=['{:,.2f} hrs'.format(x) for x in emp_df_sum["Total hours"]],
                             template="seaborn")
                st.plotly_chart(fig, use_container_width=True, height=200)

            with col2:
                st.subheader("Team wise data")
                fig = px.pie(emp_df_avg, values="Total hours", names="Team Name")
                fig.update_traces(text=filtered_df["Team Name"], textposition="outside")
                st.plotly_chart(fig, use_container_width=True)


        elif filename.__contains__('pdf'):
            pdf_reader = PdfReader(fl)











if __name__ == '__main__':
    main()