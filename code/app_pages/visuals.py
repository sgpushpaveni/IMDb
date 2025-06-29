import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import common.get_db_data as db_data
import plotly.express as px
import plotly.graph_objects as go


def get_view(selected_visual,movies_df, mySQLcursor):
    if selected_visual == "Top Rated Movies":
         get_top_rated(movies_df)
    elif selected_visual == "Explore Genre":
         get_genre(movies_df, mySQLcursor)
    elif selected_visual == "Duration Insights":
         get_duration_insights(movies_df)
    elif selected_visual == "Voting Patterns":
         get_voting_patterns(movies_df)         
    elif selected_visual == "Popular Genres":
         get_popular_genres(movies_df)
    elif selected_visual == "Rating Distribution":
         get_rating_distribution(movies_df)
    elif selected_visual == "Genre vs Votes":
         get_genre_vs_votes(movies_df)         
    elif selected_visual == "Duration Extremes":
         get_duration_extremes(movies_df)
    elif selected_visual == "Top-Voted Movies":
         get_top_voted(movies_df)           , 
    else:
        st.error(f"No view defined for {selected_visual}") 


def get_top_rated(df):
    st.title("Transaction Data Analysis")

    if (df.shape[0] > 0):
        st.write("Top 10 highest rated Movies ")
        top_list = df.nlargest(10,columns=['rating','voting'])
        st.dataframe(
            top_list[['title','genre', 'rating', 'voting']],
            hide_index=True,
            column_config= {
                "title": st.column_config.TextColumn(label="Movie Name"),
                "genre": st.column_config.TextColumn(label="Genre"),
                "rating": st.column_config.NumberColumn(label="Rating"),
                "voting": st.column_config.NumberColumn(label="Votes"),
            },
            width=450
          )
        
        st.write("Top 10 top votes Movies ")
        top_votted_list = df.nlargest(10,columns=['voting'])
        st.dataframe(
          top_votted_list[['title','genre', 'voting']].reset_index(drop=True),
          column_config= {
                "col1": st.column_config.TextColumn(label="Movie Name"),
                "col2": st.column_config.TextColumn(label="Genre"),
                "col3": st.column_config.NumberColumn(label="Votes"),
          },
          width=500,
          )
    else:
        st.error("No data available.")

def get_genre(df, mySQLcursor):
    st.title('Explore Genre')
    st.subheader("Genre Distribution")

    if (df.shape[0] > 0):
          genre_data = db_data.get_query_data(mySQLcursor, db_data.qry_genre_dist)
          genre_df = pd.DataFrame(genre_data, columns=["Genre", "Counts"])
          st.dataframe(
               genre_df,
               width=200,
               hide_index=True)
          # Create the Seaborn bar plot
          # fig, ax = plt.subplots(figsize=(4,2)) 
          # #ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='center')
          # ax.tick_params(axis='x', rotation=90)
          # ax.set_xlabel("Genre", fontsize=10)
          # ax.set_ylabel("Counts")
          # ax.set_title("Bar Plot for Genres")
          # ax.set_xticklabels(genre_df['Genre'], size=5)
          # ax.set_yticklabels(genre_df['Counts'], size=5)
          # sns.barplot(x='Genre', y='Counts', data=genre_df, ax=ax, palette='viridis')
          # st.pyplot(fig,use_container_width=False)

          genre_counts = df["genre"].value_counts().reset_index()
          genre_counts.columns = ["Genre", "Count"]
          st.plotly_chart(px.bar(genre_counts, x="Genre", y="Count", title="Number of Movies per Genre"))
    else:
        st.warning("No data available.")

def get_top_voted(df):
    st.title("Top 10 highest Voted Movies")
    if (df.shape[0] > 0):
        top_votted_list = df.nlargest(10,columns=['voting'])
        st.dataframe(top_votted_list[['title','genre', 'voting']],hide_index=True)
        
        bar_plot = px.bar(top_votted_list,x='title', y='voting',hover_data='voting',title='Top votted movies')
        st.plotly_chart(bar_plot)
    else:   
        st.error("No data available.")

def get_duration_insights(df):
     st.title('Duration Insights')
     avg_duration = df.groupby("genre")["duration"].mean().reset_index()
     st.plotly_chart(px.bar(avg_duration, x="duration", y="genre", orientation="h", title="Average Duration per Genre"))

def get_voting_patterns(df):
     st.title('Voting Patterns')
     avg_voting = df.groupby("genre")["voting"].mean().reset_index()
     #st.dataframe(avg_voting)
     st.plotly_chart(px.bar(avg_voting, x="genre", y="voting", title="Average Voting Counts per Genre"))

def get_popular_genres(df):
     st.title('Popular Genres')
     genre_counts = df["genre"].value_counts().reset_index()
     genre_counts.columns = ["Genre", "Movies Count"]
     st.dataframe(genre_counts,hide_index=True, width=300)
    
def get_rating_distribution(df):
     st.title('Rating Distribution')
     st.plotly_chart(px.histogram(df, x="rating", nbins=20, title="Rating Distribution of Movies"))

def get_genre_vs_votes(df):
     st.title('Genre vs. Votes')
     total_votes_by_genre = df.groupby("genre")["voting"].sum().reset_index()
     #st.dataframe(total_votes_by_genre)
     st.plotly_chart(px.pie(total_votes_by_genre, names="genre", values="voting", title="Most Popular Genres by Voting"))

def get_duration_extremes(df):
     st.title('Duration Extremes')
     # Filter out movies with valid durations (> 0)
     valid_movies = df[df["duration"] > 0]

     # Get the shortest and longest movies from valid entries
     shortest_movie = valid_movies.loc[valid_movies["duration"].idxmin()]
     longest_movie = valid_movies.loc[valid_movies["duration"].idxmax()]

     st.subheader("Shortest & Longest Movies")

     col1, col2 = st.columns(2)

     with col1:
          st.markdown("### 🎬 Shortest Movie")
          st.markdown(f"**Title:** {shortest_movie['title']}")
          st.markdown(f"**Duration:** ⏳ {shortest_movie['duration']} mins")
          st.markdown(f"**Rating:** ⭐ {shortest_movie['rating']}")
          st.markdown(f"**Genre:** 🎭 {shortest_movie['genre']}")
          st.markdown("---")

     with col2:
          st.markdown("### 🎬 Longest Movie")
          st.markdown(f"**Title:** {longest_movie['title']}")
          st.markdown(f"**Duration:** ⏳ {longest_movie['duration']} mins")
          st.markdown(f"**Rating:** ⭐ {longest_movie['rating']}")
          st.markdown(f"**Genre:** 🎭 {longest_movie['genre']}")
          st.markdown("---")



     # Ratings by Genre (Heatmap)
     st.subheader("🎨 Ratings by Genre ")
     heatmap_data = df.pivot_table(index="genre", values="rating", aggfunc="mean").reset_index()
     st.plotly_chart(px.imshow([heatmap_data["rating"]], labels=dict(x="genre", y="Average Rating"), x=heatmap_data["genre"]))

     # Correlation Analysis
     st.subheader("📊 Correlation: Ratings vs Voting")
     st.plotly_chart(px.scatter(df, x="voting", y="rating", title="Correlation Between Ratings & Voting Counts"))

     st.plotly_chart(px.bar(df, x="voting", y="rating", title="Correlation Between Ratings & Voting Counts"))
     st.plotly_chart(px.bar(df, x="voting", y="rating", title="Correlation Between Ratings & Voting Counts"))
























