"""Page Année 2025-26 : point d'entrée vers ses sous-menus."""

import streamlit as st

st.title("Année 2025-26")
st.markdown(
    "Les documents de l'année 2025-26 (suivi du budget, dépenses courantes, "
    "travaux, résolutions et documents) sont rattachés à l'**AG-2026**."
)
st.page_link("pages/1_AG_2026.py", label="AG-2026", icon="🗳️")
st.page_link(
    "pages/1_Journal_2025_26.py", label="Journal des interventions", icon="🛠️"
)
