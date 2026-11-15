"""Page Vigik+ (année 2026-27)."""

import streamlit as st

from views.annee import DATA_DIR, render_documents

st.title("Vigik+")
render_documents(DATA_DIR / "2026-27" / "vigik+", "vigik_2026-27")
