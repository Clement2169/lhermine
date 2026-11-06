"""Point d'entrée — navigation Résidence l'Hermine."""

import streamlit as st

st.set_page_config(
    page_title="Résidence l'Hermine",
    page_icon="🏠",
    layout="wide",
)

accueil = st.Page("views/accueil.py", title="Résidence l'Hermine", icon="🏠", default=True)
annee_2025_26 = st.Page(
    "pages/1_Année_2025_26.py", title="Année 2025-26", icon="📅"
)
annee_2026_27 = st.Page(
    "pages/2_Année_2026_27.py", title="Année 2026-27", icon="📅"
)

pg = st.navigation(pages=[accueil, annee_2025_26, annee_2026_27], position="sidebar")
pg.run()
