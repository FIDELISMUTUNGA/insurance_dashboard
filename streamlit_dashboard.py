import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Title
st.title("Insurance Dataset Interactive Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv(r"insurance.csv")
    return df

df = load_data()

# Sidebar for filters
st.sidebar.header("Filters")

region = st.sidebar.multiselect("Select Region", options=df['region'].unique(), default=df['region'].unique())
smoker = st.sidebar.multiselect("Select Smoker Status", options=df['smoker'].unique(), default=df['smoker'].unique())
sex = st.sidebar.multiselect("Select Sex", options=df['sex'].unique(), default=df['sex'].unique())
age_range = st.sidebar.slider("Select Age Range", min_value=int(df['age'].min()), max_value=int(df['age'].max()), value=(int(df['age'].min()), int(df['age'].max())))

# Filter data
filtered_df = df[
    (df['region'].isin(region)) &
    (df['smoker'].isin(smoker)) &
    (df['sex'].isin(sex)) &
    (df['age'] >= age_range[0]) &
    (df['age'] <= age_range[1])
]

# Data summary
st.header("Data Summary")
st.write(f"Total records: {len(filtered_df)}")
st.write(filtered_df.describe())

# Plots
st.header("Visualizations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Age vs Charges")
    fig1 = px.scatter(filtered_df, x='age', y='charges', color='smoker', title='Age vs Charges')
    st.plotly_chart(fig1)

with col2:
    st.subheader("BMI Distribution")
    fig2 = px.histogram(filtered_df, x='bmi', title='BMI Distribution')
    st.plotly_chart(fig2)

st.subheader("Charges by Number of Children")
fig3 = px.box(filtered_df, x='children', y='charges', title='Charges by Number of Children')
st.plotly_chart(fig3)

st.subheader("Charges by Region")
fig4 = px.bar(filtered_df.groupby('region')['charges'].mean().reset_index(), x='region', y='charges', title='Average Charges by Region')
st.plotly_chart(fig4)
