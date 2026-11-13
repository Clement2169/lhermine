"""Contenu commun des pages d'assemblée générale.

Une AG reprend les documents de l'exercice qu'elle clôt : l'AG-2026 affiche
ceux de l'année 2025-26 (budget, dépenses, travaux, résolutions, documents).
"""

import streamlit as st

from views.annee import render_onglets


def render_ag(annee: str, ag: str) -> None:
    """Affiche la page d'une AG, par exemple ``render_ag("2025-26", "AG2026")``."""
    st.title(f"Assemblée générale {ag[2:]}")
    st.caption(f"Documents de l'exercice {annee}.")
    render_onglets(annee)
