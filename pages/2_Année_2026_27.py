"""Page Année 2026-27 : point d'entrée vers ses sous-menus."""

import streamlit as st

st.title("Année 2026-27")
st.markdown(
    "Les documents de l'année 2026-27 (suivi du budget, dépenses courantes, "
    "travaux, résolutions et documents) sont rattachés à l'**AG-2027**."
)
st.page_link("pages/2_AG_2027.py", label="AG-2027", icon="🗳️")
st.page_link("pages/2_Vigik_plus.py", label="Vigik+", icon="🔑")
st.page_link(
    "pages/2_Bornes_rechargeables.py", label="Bornes rechargeables", icon="🔌"
)
st.page_link(
    "pages/2_Journal_2026_27.py", label="Journal des interventions", icon="🛠️"
)
