"""Page Journal des interventions (année 2026-27)."""

import streamlit as st

from views.annee import render_journal

st.title("Journal des interventions 2026-27")
render_journal("2026-27", "JournalDesInterventions2026-2027.csv")
