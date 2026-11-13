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
ag_2026 = st.Page("pages/1_AG_2026.py", title="AG-2026", icon="🗳️")
journal_2025_26 = st.Page(
    "pages/1_Journal_2025_26.py", title="Journal des interventions", icon="🛠️"
)
annee_2026_27 = st.Page(
    "pages/2_Année_2026_27.py", title="Année 2026-27", icon="📅"
)
journal_2026_27 = st.Page(
    "pages/2_Journal_2026_27.py", title="Journal des interventions", icon="🛠️"
)

# Arbre du menu : chaque page, suivie de ses sous-pages.
MENU = [
    (accueil, []),
    (annee_2025_26, [ag_2026, journal_2025_26]),
    (annee_2026_27, [journal_2026_27]),
]

# Le menu natif de Streamlit n'imbrique pas les pages : il est masqué et
# remplacé par des liens, les sous-pages étant décalées vers la droite.
pg = st.navigation(
    pages=[page for parent, enfants in MENU for page in [parent, *enfants]],
    position="hidden",
)

with st.sidebar:
    st.html("<style>[class*='st-key-sous_menu_'] { padding-left: 1.5rem; }</style>")
    for index, (parent, enfants) in enumerate(MENU):
        st.page_link(parent)
        if enfants:
            with st.container(key=f"sous_menu_{index}"):
                for enfant in enfants:
                    st.page_link(enfant)

pg.run()
