"""Page Journal des interventions (année 2025-26)."""

import streamlit as st

from views.annee import render_journal

st.title("Journal des interventions 2025-26")
render_journal("2025-26", "JournalDesInterventions2025-2026.csv")
