import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Load datasets
df_techniques_and_tactics = pd.read_csv("C:/Users/bangl/OneDrive/Máy tính/project30016/dada/Techniques_and_Tactics.csv")
df_techniques_and_groups = pd.read_csv("C:/Users/bangl/OneDrive/Máy tính/project30016/dada/Techniques_and_Groups.csv")
df_techniques_and_software = pd.read_csv("C:/Users/bangl/OneDrive/Máy tính/project30016/dada/Techniques_and_Software.csv")

# Sidebar for modular navigation
st.sidebar.title("Modular Threat Mapping Dashboard")
selected_module = st.sidebar.selectbox("Select Module", ["Top Techniques", "Software Usage", "Adversary Group Analysis", "Relationship Analysis"])

# Aggregate function to count occurrences
def aggregate_data(df, group_column, count_column):
    aggregated_data = df.groupby(group_column)[count_column].count().reset_index(name='count').sort_values(by='count', ascending=False)
    return aggregated_data

# Initialize session state for selected techniques to prevent random reselection
if 'selected_techniques' not in st.session_state:
    # Technique Selection
    all_techniques = df_techniques_and_tactics['name'].unique()
    # Select 5 random techniques by default only the first time
    st.session_state.selected_techniques = random.sample(list(all_techniques), 5)

# Module 1: Top Techniques Visualization
if selected_module == "Top Techniques":
    st.title("Top Techniques Across Groups")
    
    # Aggregate the data to find the top 10 most frequently used techniques
    top_techniques = df_techniques_and_groups.groupby('target name').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    
    # Display the top 10 techniques
    st.write("Displaying top 10 most used techniques across groups")
    fig_top = px.bar(top_techniques, x='target name', y='count', title="Top 10 Techniques", labels={'target name': 'Technique', 'count': 'Occurrences'})
    st.plotly_chart(fig_top)

# Module 2: Software Usage Visualization
elif selected_module == "Software Usage":
    st.title("Software Usage Across Techniques")
    
    # Aggregate software usage data
    software_usage = df_techniques_and_software.groupby('name_software').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    
    # Display the software usage data
    st.write("Displaying top 10 most frequently used software across techniques")
    fig_software = px.bar(software_usage, x='name_software', y='count', title="Top 10 Software", labels={'name_software': 'Software', 'count': 'Occurrences'})
    st.plotly_chart(fig_software)

# Module 3: Adversary Group Analysis
elif selected_module == "Adversary Group Analysis":
    st.title("Adversary Group Usage Across Techniques")
    
    # Aggregate adversary group data
    group_usage = df_techniques_and_groups.groupby('source name').size().reset_index(name='count').sort_values(by='count', ascending=False).head(10)
    
    # Display adversary group data
    st.write("Displaying top 10 most active adversary groups across techniques")
    fig_group = px.bar(group_usage, x='source name', y='count', title="Top 10 Adversary Groups", labels={'source name': 'Adversary Group', 'count': 'Occurrences'})
    st.plotly_chart(fig_group)

# Module 4: Relationship Analysis (Using Stacked Bar, Scatter Plot, and Treemap)
elif selected_module == "Relationship Analysis":
    st.title("Relationship Between Techniques, Tactics, and Software")
    
    # Technique Selection: Allow user to choose techniques but preselect 5 random ones the first time
    selected_techniques = st.multiselect(
        "Select techniques to compare (default 5 random):", 
        options=df_techniques_and_tactics['name'].unique(), 
        default=st.session_state.selected_techniques
    )

    # Update session state when user makes a selection
    if selected_techniques:
        st.session_state.selected_techniques = selected_techniques

    # Filter data based on selected techniques
    filtered_tactics_data = df_techniques_and_tactics[df_techniques_and_tactics['name'].isin(st.session_state.selected_techniques)]
    filtered_groups_data = df_techniques_and_groups[df_techniques_and_groups['target name'].isin(st.session_state.selected_techniques)]
    filtered_software_data = df_techniques_and_software[df_techniques_and_software['name_technique'].isin(st.session_state.selected_techniques)]

    # Stacked Bar Chart: Techniques grouped by Tactics
    st.subheader("Stacked Bar Chart: Techniques Grouped by Tactics")
    stacked_data = filtered_tactics_data.groupby(['tactics', 'name']).size().reset_index(name='count')
    fig_stacked = px.bar(stacked_data, x='tactics', y='count', color='name', title="Techniques Grouped by Tactics (Stacked Bar Chart)")
    st.plotly_chart(fig_stacked)
    
    # Scatter Plot: Techniques vs Adversary Groups
    st.subheader("Scatter Plot: Techniques vs Adversary Groups")
    scatter_data = filtered_groups_data.groupby(['target name', 'source name']).size().reset_index(name='count')
    fig_scatter = px.scatter(scatter_data, x='source name', y='target name', size='count', color='count', title="Techniques vs Adversary Groups (Scatter Plot)")
    st.plotly_chart(fig_scatter)
    
    # Treemap: Visualizing Techniques by Software
    st.subheader("Treemap: Techniques by Software")
    treemap_data = filtered_software_data.groupby(['name_software', 'name_technique']).size().reset_index(name='count')
    fig_treemap = px.treemap(treemap_data, path=['name_software', 'name_technique'], values='count', title="Techniques by Software (Treemap)")
    st.plotly_chart(fig_treemap)
