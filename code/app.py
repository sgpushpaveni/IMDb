import streamlit as st
import altair as alt
import mysql.connector
import pandas as pd

import app_pages.visuals as data_visuals
import app_pages.filters as filters
import common.get_db_data as db_data

db_name = "imdb"
movies_table = "movies"

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database=db_name
)

mySQLcursor = connection.cursor()

data_movies = db_data.get_table_data(mySQLcursor, movies_table)
column_names = ['genre', 'year', 'title', 'duration', 'certificate', 'rating', 'voting' ]
movies_df = pd.DataFrame(data_movies, columns=column_names)

# Streamlit App Title
st.set_page_config(
    page_title="IMDB Data Scraping and Visualizations (2024 - Movies)", 
    layout="wide",
    initial_sidebar_state="expanded", #"collapsed","expanded",
    page_icon="random"
)

# Inject custom CSS to reduce padding and margins
custom_css = """
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    <p>Phonepe EDA</p>
    .main .block-container {
        max-width: 100%;
    }
</style>
"""
logo = '''
![logo]|("logo.svg")
'''
st.markdown(custom_css, unsafe_allow_html=True)
#st.markdown(logo, unsafe_allow_html=True)
alt.themes.enable("dark")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("IMDB Movies Insights", 
                        ["Project Introduction", 
                         "Interactive Visualizations",
                         "Interactive Filtering", 
                         "App Info"]
                         )

visuals_list = ["Top Rated Movies", 
                "Explore Genre", 
                "Duration Insights", 
                "Voting Patterns", 
                "Popular Genres", 
                "Rating Distribution", 
                "Genre vs Votes", 
                "Duration Extremes", 
                "Top-Voted Movies" ]


# -------------------------------- PAGE: Introduction --------------------------------
if page == "Project Introduction":
    st.title("IMDB Data Scraping and Visualizations for 2024 Movies")
    st.subheader("An Streamlit App to show the Insights of Movies")
    st.write("""
    **Problem Statement:**
    * Scraping data such as movie names, genres, ratings, voting counts, and durations from IMDb's 2024 movie list using Selenium. 
    * Organizing genre-wise data in separate CSV files
    * Combining the data into a single dataset and storeing in an SQL database.
    * Aiming to provide interactive visualizations and filtering functionality using Streamlit.
             
    **Business Use Cases:**
    * Top-Rated Movies: Identify the top 10 movies with the highest ratings and voting counts.
    * Genre Analysis: Explore the distribution of genres in the 2024 movie list.
    * Duration Insights: Analyze the average duration of movies across genres.
    * Voting Patterns: Discover genres with the highest average voting counts.
    * Popular Genres: Identify the genres that dominate IMDb's 2024 list based on movie count.
    * Rating Distribution: Analyze the distribution of ratings across all movies.
    * Genre vs. Ratings: Compare the average ratings for each genre.
    * Duration Extremes: Identify the shortest and longest movies in 2024.
    * Top-Voted Movies: Find the top 10 movies with the highest voting counts.
    * Interactive Filtering: Allow users to filter movies by ratings, duration, votes, and genre and view the results in a tabular DataFrame format.

    
    **Technologies & Techniques Used:**
    * Selenium 
    * MySQL - `IMDB.MySQL`
    * Streamlit 
    * Python 
        * Pandas 
        * Data Cleaning 
        * Data Analysis 
        * Visualization 
        * Interactive Filters
    """)

# -------------------------------- PAGE: Top rated movies --------------------------------
elif page == "Interactive Visualizations":
    selected_visual = st.sidebar.selectbox('Select a Visualization', visuals_list)
    data_visuals.get_view(selected_visual, movies_df, mySQLcursor)

# -------------------------------- PAGE: Interactive Filtering --------------------------------
elif page == "Interactive Filtering":
    filters.get_filters(mySQLcursor)

# -------------------------------- PAGE: App Info --------------------------------
elif page == "App Info":
    st.title("App information")
    st.write("""
    **Developed by:** SG Pushpaveni \n\n
    **Skills:** Python MySQL Data Analysis Streamlit Pandas
    """)
