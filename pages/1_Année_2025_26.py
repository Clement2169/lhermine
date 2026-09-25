"""Page Année 2025-26."""

from pathlib import Path

import pandas as pd
import streamlit as st

JOURNAL_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "journaux"
    / "JournalDesInterventions2025-2026.csv"
)


@st.cache_data
def load_journal(path: str) -> pd.DataFrame:
    """Charge le journal des interventions (UTF-8 puis repli CP1252)."""
    try:
        df = pd.read_csv(
            path, encoding="utf-8-sig", dtype=str, keep_default_na=False
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            path, encoding="cp1252", dtype=str, keep_default_na=False
        )
    df.columns = ["date", "objet", "demandeur", "intervenant", "commentaire"][
        : len(df.columns)
    ]
    return df.apply(lambda col: col.str.strip() if col.dtype == object else col)

st.title("Année 2025-26")

tab_budget, tab_depenses, tab_travaux, tab_journal, tab_docs = st.tabs(
    [
        "Suivi du budget",
        "Dépenses courantes",
        "Travaux",
        "Journal des interventions",
        "Documents",
    ]
)

with tab_budget:
    st.subheader("Suivi du budget")
    st.markdown(
        """
        Synthèse du budget de l'année **2025-26**.

        Ajoutez ici vos tableaux et indicateurs (prévu / réalisé / solde…).
        """
    )

with tab_depenses:
    st.subheader("Dépenses courantes")
    st.markdown(
        """
        Liste des dépenses courantes de l'année **2025-26**.

        Ajoutez ici vos lignes de dépenses (date, libellé, montant…).
        """
    )

with tab_travaux:
    st.subheader("Travaux")
    st.markdown(
        """
        Suivi des travaux de l'année **2025-26**.

        Ajoutez ici vos travaux (description, statut, coût…).
        """
    )

with tab_journal:
    st.subheader("Journal des interventions")
    if not JOURNAL_PATH.is_file():
        st.error(f"Fichier introuvable : {JOURNAL_PATH}")
    else:
        df_journal = load_journal(str(JOURNAL_PATH))
        st.caption(f"{len(df_journal)} interventions — {JOURNAL_PATH.name}")
        st.markdown(
            """
            <style>
            div[data-testid="block-container"] { max-width: 100%; padding-left: 2rem; padding-right: 2rem; }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(
            df_journal,
            use_container_width=True,
            hide_index=True,
            height=600,
            column_config={
                "date": st.column_config.TextColumn("Date", width="small"),
                "objet": st.column_config.TextColumn("Objet", width="large"),
                "demandeur": st.column_config.TextColumn("Demandeur", width="medium"),
                "intervenant": st.column_config.TextColumn(
                    "Intervenant", width="medium"
                ),
                "commentaire": st.column_config.TextColumn(
                    "Commentaire", width="medium"
                ),
            },
        )

with tab_docs:
    st.subheader("Documents")
    st.markdown(
        """
        Documents de l'année **2025-26**.

        Ajoutez ici vos documents (comptes rendus, factures, devis…).
        """
    )
