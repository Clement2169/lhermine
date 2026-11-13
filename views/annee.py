"""Contenu commun des pages d'année (5 onglets) et du journal des interventions."""

from html import escape
from io import StringIO
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
JOURNAUX_DIR = DATA_DIR / "journaux"
DOCUMENTS_DIR = DATA_DIR / "documents"
BUDGET_DIR = DATA_DIR / "budget"
DEPENSES_DIR = DATA_DIR / "depenses"
RESOLUTIONS_DIR = DATA_DIR / "resolutions"
TRAVAUX_DIR = DATA_DIR / "travaux"

# Une liste de fichiers ne passe sur deux colonnes qu'au-delà de ce nombre.
MAX_FILES_ONE_COLUMN = 5

# st.pdf s'ouvre toujours à 100 % et n'a pas d'option de zoom initial : ce script
# clique sur son bouton « + » (25 % par clic) pour agrandir chaque PDF ouvert
# autant que possible, jusqu'à 175 %, tant que les pages tiennent dans le lecteur.
# Le lecteur centre tout PDF comme un portrait, ce qui décale les pages paysage
# vers la droite : le script les ramène ensuite dans la zone visible.
# Si le bouton n'est pas trouvé, le PDF reste simplement à 100 %.
PDF_ZOOM_SCRIPT = """
<script data-document="{document}">
(() => {{
  const ZOOM_STEP = 0.25;
  const MAX_STEPS = 3;
  const MARGIN = 24; // place de la barre de défilement
  const WAIT_TICKS = 5; // laisse le temps à plusieurs pages de s'afficher
  const findZoomInButtons = (root) => {{
    const buttons = [...root.querySelectorAll('button[title="Zoom In"]')];
    for (const element of root.querySelectorAll("*")) {{
      if (element.shadowRoot) buttons.push(...findZoomInButtons(element.shadowRoot));
    }}
    return buttons;
  }};
  const showWholePage = (viewer) => {{
    const scroller = [...viewer.querySelectorAll("*")].find(
      (element) =>
        element.scrollWidth > element.clientWidth &&
        getComputedStyle(element).overflowX === "auto",
    );
    if (scroller) scroller.scrollLeft = scroller.scrollWidth;
  }};
  const ticks = new WeakMap();
  let attempts = 0;
  const timer = setInterval(() => {{
    for (const button of findZoomInButtons(document)) {{
      const viewer = button.closest('[data-testid="pdf-container"]');
      if (!viewer || viewer.dataset.zoomed) continue;
      const widths = [...viewer.querySelectorAll("canvas")]
        .map((canvas) => canvas.getBoundingClientRect().width)
        .filter((width) => width > 0);
      if (!widths.length) continue;
      ticks.set(viewer, (ticks.get(viewer) || 0) + 1);
      if (ticks.get(viewer) < WAIT_TICKS) continue;
      viewer.dataset.zoomed = "true";
      const pageWidth = Math.max(...widths);
      const maxScale = (viewer.clientWidth - MARGIN) / pageWidth;
      const steps = Math.floor((maxScale - 1) / ZOOM_STEP);
      for (let i = 0; i < Math.min(steps, MAX_STEPS); i++) button.click();
      if (pageWidth * (1 + Math.max(steps, 0) * ZOOM_STEP) <= viewer.clientWidth) {{
        setTimeout(() => showWholePage(viewer), 800);
      }}
    }}
    if (++attempts > 75) clearInterval(timer);
  }}, 200);
}})();
</script>
"""


def list_documents(directory: Path) -> list[str]:
    """Liste les fichiers de ``directory``, triés par nom.

    Ignore les fichiers cachés et les ``:Zone.Identifier`` créés par Windows.
    """
    if not directory.is_dir():
        return []
    return sorted(
        path.name
        for path in directory.iterdir()
        if path.is_file()
        and not path.name.startswith(".")
        and not path.name.endswith(":Zone.Identifier")
    )


@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    """Charge un CSV en texte (UTF-8 puis repli CP1252).

    Le séparateur est celui qui revient le plus sur la ligne d'en-tête : Excel
    en français exporte avec des points-virgules. Les colonnes sans en-tête
    sont nommées d'après leur position (« Colonne 3 »).
    """
    raw = Path(path).read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1252", errors="replace")
    header = text.partition("\n")[0]
    separator = max(",;\t", key=header.count)
    df = pd.read_csv(
        StringIO(text), sep=separator, dtype=str, keep_default_na=False
    )
    df.columns = [
        f"Colonne {position}" if name.startswith("Unnamed:") else name
        for position, name in enumerate(df.columns, start=1)
    ]
    return df.apply(lambda col: col.str.strip())


def load_journal(path: str) -> pd.DataFrame:
    """Charge le journal des interventions avec ses noms de colonnes."""
    df = load_csv(path)
    df.columns = ["date", "objet", "demandeur", "intervenant", "commentaire"][
        : len(df.columns)
    ]
    return df


def show_document(path: Path) -> None:
    """Affiche un PDF dans une zone défilante, ou un CSV sous forme de tableau."""
    st.subheader(path.name)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        st.pdf(path, height=800, key=f"pdf_{path}")
        st.html(
            PDF_ZOOM_SCRIPT.format(document=escape(str(path), quote=True)),
            unsafe_allow_javascript=True,
        )
    elif suffix == ".csv":
        try:
            df = load_csv(str(path))
        except (pd.errors.ParserError, pd.errors.EmptyDataError):
            st.warning(
                "Ce fichier CSV ne peut pas être affiché : il est vide ou mal "
                "formé. Vous pouvez toujours le télécharger."
            )
            return
        st.caption(f"{len(df)} lignes")
        st.dataframe(df, width="stretch", hide_index=True, height=600)
    else:
        st.info("Aperçu indisponible pour ce type de fichier.")


def render_documents(directory: Path, key: str, columns: int = 2) -> None:
    """Liste les fichiers d'un dossier : un clic affiche le fichier en dessous.

    Au-delà de ``MAX_FILES_ONE_COLUMN`` fichiers, la liste est répartie sur
    ``columns`` colonnes (deux par défaut), remplies l'une après l'autre pour
    garder l'ordre alphabétique de haut en bas.
    """
    documents = list_documents(directory)
    if not documents:
        st.info(
            "Aucun document pour le moment : ajoutez vos fichiers "
            f"dans {directory.relative_to(PROJECT_DIR).as_posix()}/."
        )
        return

    selected_key = f"selected_{key}"
    if len(documents) <= MAX_FILES_ONE_COLUMN:
        columns = 1
    per_column = -(-len(documents) // columns)  # division arrondie au supérieur
    cols = st.columns(columns) if columns > 1 else [st.container()]
    for index, name in enumerate(documents):
        column = cols[index // per_column]
        with column, st.container(horizontal=True, vertical_alignment="center"):
            if st.button(
                name,
                key=f"open_{key}_{name}",
                type="tertiary",
                icon=":material/description:",
            ):
                st.session_state[selected_key] = name
            st.download_button(
                "Télécharger",
                data=(directory / name).read_bytes,
                file_name=name,
                key=f"download_{key}_{name}",
                on_click="ignore",
                icon=":material/download:",
            )

    selected = st.session_state.get(selected_key)
    if selected in documents:
        st.divider()
        show_document(directory / selected)


def render_journal(annee: str, journal_filename: str) -> None:
    """Affiche le journal des interventions d'une année."""
    journal_path = JOURNAUX_DIR / journal_filename
    if not journal_path.is_file():
        st.info(
            "Aucun journal pour le moment : ajoutez "
            f"{journal_filename} dans data/journaux/."
        )
    else:
        df_journal = load_journal(str(journal_path))
        st.caption(f"{len(df_journal)} interventions — {journal_path.name}")
        st.download_button(
            "Télécharger",
            data=journal_path.read_bytes,
            file_name=journal_path.name,
            mime="text/csv",
            key=f"download_journal_{annee}",
            on_click="ignore",
            icon=":material/download:",
        )
        st.dataframe(
            df_journal,
            use_container_width=True,
            hide_index=True,
            height=600,
            column_config={
                "date": st.column_config.TextColumn("Date", width="small"),
                "objet": st.column_config.TextColumn("Objet", width="large"),
                "demandeur": st.column_config.TextColumn(
                    "Demandeur", width="medium"
                ),
                "intervenant": st.column_config.TextColumn(
                    "Intervenant", width="medium"
                ),
                "commentaire": st.column_config.TextColumn(
                    "Commentaire", width="medium"
                ),
            },
        )


def render_annee(annee: str) -> None:
    """Affiche la page d'une année, par exemple ``render_annee("2026-27")``.

    Le journal des interventions n'en fait pas partie : il a sa propre page,
    en sous-menu de l'année (voir ``render_journal``).
    """
    st.title(f"Année {annee}")
    render_onglets(annee)


def render_onglets(annee: str) -> None:
    """Affiche les 5 onglets de documents d'une année.

    Utilisé par la page de l'année, ou par celle de son assemblée générale
    quand les documents de l'année lui sont rattachés (2025-26 → AG-2026).
    """
    # Les dossiers budget, dépenses et travaux utilisent l'année complète : 2026-2027.
    debut, fin = annee.split("-")
    annee_complete = f"{debut}-{debut[:2]}{fin}"

    noms = ["Suivi du budget", "Dépenses courantes", "Travaux", "Résolutions", "Documents"]
    tabs = dict(zip(noms, st.tabs(noms)))

    with tabs["Suivi du budget"]:
        st.subheader("Suivi du budget")
        render_documents(BUDGET_DIR / annee_complete, f"budget_{annee}")

    with tabs["Dépenses courantes"]:
        st.subheader("Dépenses courantes")
        render_documents(DEPENSES_DIR / annee_complete, f"depenses_{annee}")

    with tabs["Travaux"]:
        st.subheader("Travaux")
        render_documents(TRAVAUX_DIR / annee_complete, f"travaux_{annee}")

    with tabs["Résolutions"]:
        st.subheader("Résolutions")
        render_documents(RESOLUTIONS_DIR / annee, f"resolutions_{annee}")

    with tabs["Documents"]:
        st.subheader("Documents")
        render_documents(DOCUMENTS_DIR / annee, f"documents_{annee}")
