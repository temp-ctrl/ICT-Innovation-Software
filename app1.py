import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
df_techniques_and_tactics = pd.read_csv("C:/Users/bangl/OneDrive/Máy tính/project30016/dada/Techniques_and_Tactics.csv")
df_techniques_and_groups = pd.read_csv("C:/Users/bangl/OneDrive/Máy tính/project30016/dada/Techniques_and_Groups.csv")
df_techniques_and_software = pd.read_csv("C:/Users/bangl/OneDrive/Máy tính/project30016/dada/Techniques_and_Software.csv")

# Sidebar for modular navigation
st.sidebar.title("Modular Threat Mapping Dashboard")
selected_module = st.sidebar.selectbox("Select Module", ["Trend Over Time", "Top Techniques"])

# Aggregate function to count occurrences
def aggregate_data(df, group_column, count_column):
    aggregated_data = df.groupby(group_column)[count_column].count().reset_index(name='count').sort_values(by='count', ascending=False)
    return aggregated_data

# Module 1: Trend Over Time Visualization
if selected_module == "Trend Over Time":
    st.title("Trend Over Time for Techniques")
    
    # If 'created' and 'last modified' fields exist, visualize how techniques are used over time
    if 'created' in df_techniques_and_groups.columns:
        df_techniques_and_groups['created'] = pd.to_datetime(df_techniques_and_groups['created'])
        df_techniques_and_groups['year'] = df_techniques_and_groups['created'].dt.year
        
        # Group data by year and count occurrences of each technique
        trend_data = df_techniques_and_groups.groupby('year')['target name'].count().reset_index(name='count')
        
        # Display trend data
        st.write("Displaying the trend of techniques usage over time:")
        fig_trend = px.line(trend_data, x='year', y='count', title="Techniques Usage Over Time", labels={'count': 'Occurrences'})
        st.plotly_chart(fig_trend)
    else:
        st.write("The dataset does not contain a 'created' field to show a time trend.")
# Module 2: Top Techniques Visualization
elif selected_module == "Top Techniques":
    st.title("Top Techniques Across Groups and Software")
    
    # Aggregate the data to find the top 10 most frequently used techniques
    top_techniques = df_techniques_and_groups.groupby('target name').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    
    # Display the top 10 techniques
    st.write("Displaying top 10 most used techniques across groups")
    fig_top = px.bar(top_techniques, x='target name', y='count', title="Top 10 Techniques", labels={'target name': 'Technique', 'count': 'Occurrences'})
    st.plotly_chart(fig_top)
