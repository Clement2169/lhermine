"""Page Bornes rechargeables (année 2026-27)."""

import streamlit as st

from views.annee import DATA_DIR, render_documents

st.title("Bornes rechargeables")
render_documents(DATA_DIR / "2026-27" / "bornes-rechargeables", "bornes_2026-27")
