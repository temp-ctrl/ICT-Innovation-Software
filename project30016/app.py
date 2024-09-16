# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
file_path = r"C:/Users/User/OneDrive/Máy tính/project30016/dada/Techniques_and_Tactics.csv"
techniques_tactics_df = pd.read_csv(file_path)

# Create a sidebar for filter options
st.sidebar.title("Filter Options")
selected_tactic = st.sidebar.selectbox("Select Tactic", techniques_tactics_df['tactics'].unique())

# Filter data based on the selected tactic
filtered_data = techniques_tactics_df[techniques_tactics_df['tactics'] == selected_tactic]

# Display a bar chart
st.write(f"Techniques used under {selected_tactic}")
fig = px.bar(filtered_data, x='name', y='ID', title=f'Techniques under {selected_tactic}')
st.plotly_chart(fig)
