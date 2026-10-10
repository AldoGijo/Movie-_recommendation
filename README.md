# 🎬 Movie Recommendation System

An interactive, data-driven **Movie Recommendation System** built using an end-to-end data engineering pipeline and a responsive **Streamlit** user dashboard. This project addresses advanced data parsing challenges by transforming nested text artifacts into optimized arrays, enabling users to explore content using flexible filtering criteria alongside traditional item-to-item content mapping matrices.

---

## 🚀 Key Level 3 Implementations

- **Dynamic Dropdowns (Zero JSON Leakage):** Resolves complex CSV text serialization issues by leveraging safe parsing utilities (`ast.literal_eval`). This maps stringified array structures back into clean Python elements, completely removing raw metadata dictionary leaks (e.g., pulling up raw fields like `{"id": 1463, "name": "culture clash"}`).
- **No Movie Input Required (Filter-Based Discovery):** Decouples the dashboard from requiring a manual title entry. Users can discover films instantly by picking a **Genre** and **Release Year** directly from clean filtering menus.
- **Dual-Mode Recommendation Architecture:**
  - **Filter Choice Discovery (Tab 1):** Subsets data based on dropdown choices and runs recommendations sorted by a combination of target metrics (`vote_average` and `popularity`).
  - **Content Similarity Mapping (Tab 2):** Uses a pre-computed item-to-item cosine similarity matrix to search and recommend similar movies based on a selected title.
- **Tabbed Layout Interface:** Organized using Streamlit’s layout architecture to separate immediate filtered browsing from core matrix similarity tracking.

---

## 🛠️ Tech Stack & Architecture

- **Backend Data Pipeline:** Python, Pandas, NumPy, Jupyter Notebook
- **Dashboard Interface:** Streamlit Engine
- **Data Serialization:** Pickle (for similarity matrix storage), AST (Abstract Syntax Tree literal parsing)
- **Recommendation Architecture:** Content-Based Filtering via Vector Cosine Similarity Matrices

---

## 📂 Project Tree Structure

```text
├── movie_recomend.ipynb   # Complete data extraction, cleaning, and matrix computation notebook
├── app.py                 # Fully fixed Streamlit application with robust runtime parsing logic
├── cleaned_movies.csv     # Preprocessed and engineered dataset mapping clean list columns
└── similarity_matrix.pkl  # Pickled structural weights mapping cosine movie relationships
```

---

## ⚡ Setup & Execution Instructions

Follow these chronological steps to configure your environment and run the application dashboard locally.

### 1. Clone the Workspace
```bash
git clone https://github.com
cd YOUR_REPOSITORY_NAME
```

### 2. Install Project Dependencies
Ensure your active environment contains all the required operational packages:
```bash
pip install streamlit pandas numpy notebook
```

### 3. Generate the Clean Workspace Pipeline
Open your Jupyter environment and run the `movie_recomend.ipynb` notebook fully from top-to-bottom. This execution generates the baseline data pipeline structures:
1. Cleans the nested dataset vectors.
2. Formats the flat text fields into clean evaluation targets (`genres_list`).
3. Exports your localized workspace assets: `cleaned_movies.csv` and `similarity_matrix.pkl`.

### 4. Boot Up the Streamlit Interface Server
Execute the application frame directly out of your localized workspace terminal profile:
```bash
streamlit run app.py
```

---

## 📊 Recommendation System Logic Breakdown

1. **Extraction & Joining:** Pulls raw structural movie metadata and user interaction logs into a centralized tabular format.
2. **Text Processing & Engineering:** Implements feature engineering to squash movie elements (cast, crew, genres, overviews) into a cohesive string index to train content models.
3. **Real-Time Data Normalization:** On startup, `app.py` actively tracks and parses entries in real-time, building unique element maps on-the-fly to guarantee dropdown selections are clean and uniform.
