import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import streamlit as st



# Define Your Streamlit App:
# Create a Python script for your Streamlit application.
# Import the necessary libraries (streamlit and pandas).
# Read the cluster and recommendation CSV files into Pandas DataFrames.

# Define Functions for Each Page:
# Create separate functions to define the content of each page (show_cluster_page and show_recommendation_page).
# Use Streamlit components like st.title, st.dataframe, and st.selectbox to display the content and interact with users.

# Create Streamlit App Logic:
# Use Streamlit's st.sidebar to create navigation buttons for switching between pages.
# Define the logic to display the appropriate page content based on user selection.

# Run the Streamlit App:
# Run the Streamlit app using streamlit run <filename>.py from the command line.

# Read CSV files
cluster_df = pd.read_csv('cluster_result.csv')
recommendation_df = pd.read_csv('recommendation_result.csv')
items_df = pd.read_csv('frq_items_result.csv')

cluster_df = cluster_df.drop(columns=['Unnamed: 0'], inplace=False)
recommendation_df = recommendation_df.drop(columns=['Unnamed: 0'], inplace=False)

def show_title_page():
    st.title('Fashion in Action')
    st.write('')
    st.write('')
    if st.button("Recommendation Page"):
        st.session_state.current_page = "Recommendation Page"
    if st.button("Cluster Page"):
        st.session_state.current_page = "Cluster Page"

    # Load and display the image

     # Load and display the image with CSS style
    st.markdown(
        f'<style> .reportview-container .main .block-container{{max-width: 100%; padding-top: 0; padding-right: 0; padding-left: 0; padding-bottom: 0;}}</style>',
        unsafe_allow_html=True,
    )

    st.image("image1.jpg", use_column_width=True)

# Define functions for each page
def show_cluster_page():
    st.title('Cluster Page')
    customer_id = st.selectbox('Select Customer ID:', cluster_df['Customer ID'].unique())
    cluster_info = cluster_df[cluster_df['Customer ID'] == customer_id]
    st.dataframe(cluster_info)
    if st.button("Back to Title Page"):
        st.session_state.current_page = "Title Page"

def show_recommendation_page():
    st.title('Recommendation Page')
    customer_id = st.selectbox('Select Customer ID:', recommendation_df['Customer ID'].unique())
    recommendation_info = recommendation_df[recommendation_df['Customer ID'] == customer_id]
    st.dataframe(recommendation_info)
    if st.button("Back to Title Page"):
        st.session_state.current_page = "Title Page"

# Main function
def main():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Title Page"

    if st.session_state.current_page == "Title Page":
        show_title_page()
    elif st.session_state.current_page == "Recommendation Page":
        show_recommendation_page()
    elif st.session_state.current_page == "Cluster Page":
        show_cluster_page()

if __name__ == '__main__':
    main()