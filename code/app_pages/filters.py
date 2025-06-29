import streamlit as st
import pandas as pd
import plotly.express as px
import common.get_db_data as db_data

column_names = ['Genre', 'Year', 'Title', 'Duration', 'Certificate', 'Rating', 'Voting' ]

def get_filters(mySQLcursor):
    data_movies = db_data.get_table_data(mySQLcursor, 'movies')
    movies_df = pd.DataFrame(data_movies, columns=column_names)
    movies_df.drop(['Certificate'], axis=1,inplace=True)

    st.title("Find Your Favorite Movies, Discover the Best! ")
    
    st.sidebar.header("Filters")
    selected_genre = st.sidebar.multiselect("Select Genre", movies_df["Genre"].unique())
    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0, 0.1)
    max_rating = st.sidebar.slider("Maximum Rating", 0.0, 10.0, 10.0, 0.1)
    min_votes = st.sidebar.slider("Minimum Votes", 0, int(movies_df["Voting"].max()), 1000, 100)
    movie_search = st.sidebar.text_input("Search Movie Name")
    duration_filter = st.sidebar.radio("Select Duration:", ["All", "< 2 hrs", "2-3 hrs", "> 3 hrs"])
    filtered_df = movies_df[
        (movies_df["Rating"] >= min_rating) &
        (movies_df["Rating"] <= max_rating) &
        (movies_df["Voting"] >= min_votes)
    ]
    if duration_filter == "< 2 hrs":
        filtered_df = filtered_df[filtered_df["Duration"] < 120]
    elif duration_filter == "2-3 hrs":
        filtered_df = filtered_df[(filtered_df["Duration"] >= 120) & (filtered_df["Duration"] <= 180)]
    elif duration_filter == "> 3 hrs":
        filtered_df = filtered_df[filtered_df["Duration"] > 180]
    if selected_genre:
        filtered_df = filtered_df[filtered_df["Genre"].isin(selected_genre)]
    if movie_search:
        filtered_df = filtered_df[filtered_df["Title"].str.contains(movie_search, case=False, na=False)]
    
    filtered_df = filtered_df.reset_index(drop=True)
    #st.dataframe(filtered_df)

    if not filtered_df.empty:
        # Top 10 Movies by Rating & Votes
        st.subheader("Top 10 Movies by Rating & Votes")
        top_movies = filtered_df.sort_values(["Rating", "Voting"], ascending=[False, False]).head(10)
        st.dataframe(top_movies,hide_index=True,width=600)

        # Genre Distribution
        st.subheader("Genre Distribution ")
        genre_counts = filtered_df["Genre"].value_counts().reset_index()
        genre_counts.columns = ["Genre", "Count"]
        st.plotly_chart(px.bar(genre_counts, x="Genre", y="Count", title="Number of Movies per Genre "))

        # Average Duration by Genre
        st.subheader("Duration Insights ")
        avg_duration = filtered_df.groupby("Genre")["Duration"].mean().reset_index()
        st.plotly_chart(px.bar(avg_duration, x="Duration", y="Genre", orientation="h", title="Average Duration per Genre "))

        # Voting Trends by Genre
        st.subheader("Voting Trends ")
        avg_voting = filtered_df.groupby("Genre")["Voting"].mean().reset_index()
        st.plotly_chart(px.bar(avg_voting, x="Genre", y="Voting", title="Average Voting Counts per Genre "))

        # Rating Distribution
        st.subheader("Rating Insights ")
        st.plotly_chart(px.histogram(filtered_df, x="Rating", nbins=20, title="Rating Distribution of Movies"))

        # Top Rated Movie per Genre
        st.subheader("Top Rated Movie in each Genre")
        top_per_genre = filtered_df.loc[filtered_df.groupby("Genre")["Rating"].idxmax()]
        st.dataframe(top_per_genre[["Genre", "Title", "Rating"]],hide_index=True, width=450)

        # Most Popular Genres by Voting
        st.subheader("Most Popular Genres by Voting ")
        total_votes_by_genre = filtered_df.groupby("Genre")["Voting"].sum().reset_index()
        st.plotly_chart(px.pie(total_votes_by_genre, names="Genre", values="Voting", title="Most Popular Genres by Voting "))

        # Shortest & Longest Movies
        valid_movies = filtered_df[filtered_df["Duration"] > 0]
        if not valid_movies.empty:
            shortest_movie = valid_movies.loc[valid_movies["Duration"].idxmin()]
            longest_movie = valid_movies.loc[valid_movies["Duration"].idxmax()]

            st.subheader("Shortest & Longest Movies")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Shortest Movie")
                st.markdown(f"**Title:** {shortest_movie['Title']}")
                st.markdown(f"**Duration:** {shortest_movie['Duration']} mins")
                st.markdown(f"**Rating:** {shortest_movie['Rating']}")
                st.markdown(f"**Genre:** {shortest_movie['Genre']}")
                st.markdown("---")

            with col2:
                st.markdown("### Longest Movie")
                st.markdown(f"**Title:** {longest_movie['Title']}")
                st.markdown(f"**Duration:** {longest_movie['Duration']} mins")
                st.markdown(f"**Rating:** {longest_movie['Rating']}")
                st.markdown(f"**Genre:** {longest_movie['Genre']}")
                st.markdown("---")

        # Ratings by Genre (Heatmap)
        st.subheader("Ratings by Genre ")
        heatmap_data = filtered_df.pivot_table(index="Genre", values="Rating", aggfunc="mean").reset_index()
        st.plotly_chart(px.imshow([heatmap_data["Rating"]], labels=dict(x="Genre", y="Average Rating"), x=heatmap_data["Genre"]))

        # Correlation Analysis
        st.subheader("Correlation: Ratings vs Voting ")
        st.plotly_chart(px.scatter(filtered_df, x="Voting", y="Rating", title="Correlation Between Ratings & Voting Counts "))
        st.plotly_chart(px.bar(filtered_df, x="Voting", y="Rating", title="Correlation Between Ratings & Voting Counts"))
        
        st.subheader("Filtered dataset used for the above visuals")
        filtered_df = filtered_df.reset_index(drop=True)
        st.dataframe(filtered_df)
        st.write(" ")
    else:
        st.warning("No movies filtered.")