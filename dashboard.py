import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_monthly_df(df):
    monthly_df = df.resample(rule='M', on='dteday').agg({"cnt": "sum"})
    monthly_df.index = monthly_df.index.strftime('%Y-%m')
    monthly_df = monthly_df.reset_index()
    monthly_df.rename(columns={"dteday": "month", "cnt": "total_rentals"}, inplace=True)
    return monthly_df

def create_season_df(df):
    season_df = df.groupby("season")["cnt"].sum().sort_values(ascending=False).reset_index()
    return season_df

def create_user_day_df(df):
    user_day_df = df.groupby("weekday")[["casual", "registered"]].sum().reset_index()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    user_day_df["weekday"] = pd.Categorical(user_day_df["weekday"], categories=day_order, ordered=True)
    user_day_df = user_day_df.sort_values("weekday")
    return user_day_df

def create_workday_hour_df(df):
    workday_hour_df = df[df['workingday'] == 1].groupby("hr")["cnt"].mean().reset_index()
    return workday_hour_df

def create_holiday_hour_df(df):
    holiday_hour_df = df[df['workingday'] == 0].groupby("hr")["cnt"].mean().reset_index()
    return holiday_hour_df

hour_df = pd.read_csv("hour_df_cleaned.csv")
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(drop=True, inplace=True)

min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()

with st.sidebar:
    st.title("Bike Rental Dashboard")
    start_date, end_date = st.date_input(
        label='Time Span',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                  (hour_df["dteday"] <= str(end_date))]


monthly_df = create_monthly_df(main_df)
season_df = create_season_df(main_df)
user_day_df = create_user_day_df(main_df)
workday_hour_df = create_workday_hour_df(main_df)
holiday_hour_df = create_holiday_hour_df(main_df)


st.header('Bike Rental Dashboard 2011-2012 🚲')

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rental", value=main_df["cnt"].sum())
with col2:
    st.metric("Casual User", value=main_df["casual"].sum())
with col3:
    st.metric("Registered User", value=main_df["registered"].sum())


st.subheader("Monthly Bike Rental Trends")
fig, ax = plt.subplots(figsize=(20, 8))
ax.plot(monthly_df["month"], monthly_df["total_rentals"], marker='o', linewidth=3, color="#8F3454")
plt.xticks(rotation=45, fontsize=20)
plt.yticks(fontsize=20)
plt.ylim(bottom=0) 
plt.tight_layout()
st.pyplot(fig)


st.subheader("Bike Rentals by Season")
colors = ["#D1507D", "#F0C3D3", "#F0C3D3", "#F0C3D3", "#F0C3D3"]

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="season", y="cnt", data=season_df, palette=colors, hue="season", legend=False, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.ticklabel_format(style='plain', axis='y')
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)

st.subheader("Total of Casual vs Registered User")
user_day_melted = user_day_df.melt(id_vars="weekday", value_vars=["casual", "registered"],
                                    var_name="user_type", value_name="count")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="weekday", y="count", hue="user_type", data=user_day_melted,
            palette=["#F0C3D3", "#D1507D"], ax=ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=12)
ax.ticklabel_format(style='plain', axis='y')
st.pyplot(fig)

st.subheader("Bike Rental Trends by Hour on Working Day/Holiday ")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(workday_hour_df["hr"], workday_hour_df["cnt"], marker='o', linewidth=3, color="#D1507D")
    ax.set_title("Working Days", loc="center", fontsize=18)
    ax.set_xticks(range(0, 24))
    ax.tick_params(axis='x', labelsize=13)
    ax.tick_params(axis='y', labelsize=14)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(holiday_hour_df["hr"], holiday_hour_df["cnt"], marker='o', linewidth=3, color="#D1507D")
    ax.set_title("Weekend/Holiday", loc="center", fontsize=18)
    ax.set_xticks(range(0, 24))
    ax.tick_params(axis='x', labelsize=13)
    ax.tick_params(axis='y', labelsize=14)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
    st.pyplot(fig)

st.caption('Copyright © Clarissa Halim Coding Camp 2026')