import streamlit as st
import pandas as pd
import pickle
import ast

# Set page configuration
st.set_page_config(
    page_title="Movie Recommender System",
    layout="centered"
)

# 1. Load the cleaned dataset and similarity matrix
@st.cache_data
def load_data():
    movies = pd.read_csv("cleaned_movies.csv")
    with open("similarity_matrix.pkl", "rb") as f:
        similarity = pickle.load(f)
    return movies, similarity

try:
    merged_df, similarity_matrix = load_data()
    
    # Helper function to safely parse the 'genres_list' string back into a true Python list
    def parse_genres_list(x):
        if pd.isna(x):
            return []
        try:
            # Converts the CSV text "['Action', 'Adventure']" back into a real list ['Action', 'Adventure']
            return ast.literal_eval(str(x))
        except:
            return []

    # Apply the parsing to a hidden working column
    merged_df['genres_parsed'] = merged_df['genres_list'].apply(parse_genres_list)

    # Recreate the mapping index for item-to-item (Tab 2) recommendations
    movie_indices = pd.Series(
        merged_df.index, 
        index=merged_df["original_title"].str.lower()
    ).drop_duplicates()

    # Recommendation logic function based on content similarity matrix
    def get_content_recommendations(movie_title, top_n=5):
        movie_title = movie_title.strip().lower()
        if movie_title not in movie_indices.index:
            return None
            
        idx = movie_indices[movie_title]
        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]
            
        similarity_scores = list(enumerate(similarity_matrix[idx]))
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        top_movie_indices = [i for i, score in sorted_scores[1:top_n+1]]
        
        return merged_df['original_title'].iloc[top_movie_indices].tolist()

    # 2. Extract completely clean unique genres for the dropdown
    all_genres = set()
    for genre_array in merged_df['genres_parsed']:
        for g in genre_array:
            if g.strip():
                all_genres.add(g.strip())
            
    sorted_genres = ['All Genres'] + sorted(list(all_genres))

    # 3. Streamlit User Interface Layout
    st.title("Movie Recommendation System")
    st.write("Filter by Genre and Year to discover top movies instantly, or search a specific film for content-based matches!")
    st.markdown("---")

    # Filters Row Layout
    col1, col2 = st.columns(2)
    
    with col1:
        selected_genre = st.selectbox("Select Genre:", sorted_genres)
        
    with col2:
        # Dynamically pull available years from the dataset
        year_list = ['All Years'] + sorted(list(merged_df['release_year'].dropna().unique().astype(int)), reverse=True)
        selected_year = st.selectbox("Select Release Year:", year_list)

    # 4. Apply Filters dynamically
    filtered_df = merged_df.copy()
    
    # Safe list comprehension filtering for genres
    if selected_genre != 'All Genres':
        filtered_df = filtered_df[filtered_df['genres_parsed'].apply(lambda x: selected_genre in x)]
        
    # Standard numerical matching for release year
    if selected_year != 'All Years':
        filtered_df = filtered_df[filtered_df['release_year'] == int(selected_year)]

    # 5. Recommendations Panel Layout
    st.subheader("Get Recommendations")
    
    tab1, tab2 = st.tabs(["Discover by Filter Choice", "Find Similar to a Specific Movie"])
    
    with tab1:
        st.write(f"Showing the highest-rated recommendations matching **{selected_genre}** from **{selected_year}**:")
        
        # Sort values based on popularity score metric and average voter rank
        discovered_movies = filtered_df.sort_values(by=['vote_average', 'popularity'], ascending=False).head(10)
        
        if not discovered_movies.empty:
            for i, row in enumerate(discovered_movies.itertuples(), 1):
                st.markdown(f"**{i}.** {row.original_title} — ⭐ Rating: {row.vote_average} ({int(row.release_year)})")
        else:
            st.warning("No movies match the selected filters combination. Try widening your dropdown parameters!")

    with tab2:
        # Generate movie title list directly out of active filters
        movie_list = sorted(filtered_df['original_title'].unique())
        selected_movie = st.selectbox(
            "Choose a base movie from the filtered option list:",
            movie_list,
            index=None,
            placeholder=f"Type or choose from {len(movie_list)} filtered titles..."
        )

        if st.button("Find Similar Movies", type="primary"):
            if selected_movie:
                with st.spinner('Calculating context similarity matrices...'):
                    recommendations = get_content_recommendations(selected_movie)
                    
                if recommendations:
                    st.success(f"Top recommendations based on your choice **{selected_movie}**:")
                    for i, movie in enumerate(recommendations, 1):
                        st.markdown(f"**{i}.** {movie}")
                else:
                    st.error("Could not calculate background similarities for this title asset.")
            else:
                st.warning("Please pick a valid specific movie asset from the selection dropdown first.")

except FileNotFoundError:
    st.error("Error: Could not locate your dataset source assets. Ensure 'cleaned_movies.csv' and 'similarity_matrix.pkl' reside inside your active workspace directory.")
