import streamlit as st


# --- PAGE SETUP ---
about_page = st.Page(
    "app_directory/Pages/🏠_Home_Page.py",
    default=True,
)
project_1_page = st.Page(
    "app_directory/Pages/🗺️_Water_Turbidity_Analysis_On_Map.py",
    title="Water Turbidity Analysis On Map",
)
project_2_page = st.Page(
    "app_directory/Pages/🚮_Detect_Underwater_Trash.py",
    title="Detect Underwater Trash",
)
project_3_page = st.Page(
    "app_directory/Pages/🚰_Detect_Water_Potability.py",
    title="Detect Water Potability",
)


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [about_page],
        "Projects": [project_1_page, project_2_page, project_3_page],
    }
)


# --- SHARED ON ALL PAGES ---



# --- RUN NAVIGATION ---
pg.run()