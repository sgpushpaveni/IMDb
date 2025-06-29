# IMDb 2024 Data Scraping & Visualization 

## Project Overview  
This project focuses on **extracting, analyzing, and visualizing** movie data from IMDb website for the year 2024.  
The movie details such as **Title, Genre, Duration, Rating, and Voting** are scraped using **Selenium**.  
The data is organized genre-wise, saved as individual **CSV files**, and combined into a single dataset **stored in an MySQL database**.  
This project provides interactive visualizations and filtering functionality using **Streamlit**   

## Technologies  
- **Programming Language**: Python  
- **Web Scraping**: Selenium  
- **Data Processing**: Pandas,numpy  
- **Database**: MySQL  
- **Visualization**: Plotly 
- **Web Application**: Streamlit  

## Business Use Cases  
 - **Top 10 Movies**: Identify highest-rated & most-voted movies.  
 - **Genre Distribution**: Analyze movie counts per genre.  
 - **Average Duration by Genre**: Find movie length variations by genre.  
 - **Voting Trends**: Discover genres with the most votes.  
 - **Popular Genres**: Identify IMDb's **most dominant genres** in 2024.  
 - **Rating Distribution**: Understand how ratings vary across movies.  
 - **Genre-Based Rating Leaders**: Find **top-rated** movies per genre.  
 - **Duration Extremes**: Identify the **shortest & longest** movies.  
 - **Ratings by Genre**: Compare **average ratings** for each genre.  
 - **Correlation Analysis**: Explore relationships between **ratings & voting counts**.  

**Interactive Customized Visualizations**:   
  Allow users to filter the dataset based on:
  - **Duration (Hrs)**: Filter movies based on their runtime (e.g., < 2 hrs, 2–3 hrs, > 3 hrs).
  - **Ratings**: Filter movies based on IMDb ratings (e.g., > 8.0).
  - **Voting Counts**: Filter based on the number of votes received (e.g., > 10,000 votes).
  - **Genre**: Filter movies within specific genres (e.g., Action, Drama).
  - **Display results**: Filtered results in a dynamic DataFrame within the Streamlit app.
  - **customized insights**: Combine filtering options so that the users can apply multiple filters 
  - **Visuals**: Display different visualizations for the filtered data:


## Installation  
### Clone the git Repository  
```bash
git clone https://github.com/yourusername/imdb-2024-analysis.git
```

### Install Dependencies
Dependencies installed for this project:
- Python 3.13+
- pip install pandas streamlit selenium numpy mysql-connector-python
- MySQL workbench

## Run the Streamlit Application
```bash
streamlit run app.py
```

## File Structure
```bash
IMDB-project/
├─ code/
│  ├─ app_pages/
│  │  ├─ __pycache__/
│  │  ├─ filters.py
│  │  └─ visuals.py
│  ├─ common/
│  │  ├─ __pycache__/
│  │  └─ get_db_data.py
│  ├─ data_scrap/
│  │  ├─ data_scraping.ipynb
│  │  └─ import_2_db.ipynb
│  └─ app.py
├─ data/
│  └─ csv/
│     ├─ 01_all_merged.csv
│     ├─ action.csv
│     ├─ adventure.csv
│     ├─ animation.csv
│     ├─ fantasy.csv
│     ├─ history.csv
│     ├─ mystery.csv
│     ├─ news.csv
│     ├─ reality-tv.csv
│     ├─ romance.csv
│     └─ talk-show.csv
└─ readme.md
```

## Usage
  - Interactive Visualizations: Explore IMDb 2024 movie trends with charts and graphs.
  - Interactive Filtering Functionality: Apply dynamic filters to analyze specific movie categories.

## Dataset
  Scraped the IMDb Movies data for 2024 and organized it in genre-wise.
  Data scrapped:
  
  - Movie Name
  - Genre
  - Ratings
  - Voting Counts
  - Duration

## 📽️ Project demo

