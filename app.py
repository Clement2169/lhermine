"""Point d'entrée — navigation Résidence l'Hermine."""

import hmac

import streamlit as st

st.set_page_config(
    page_title="Résidence l'Hermine",
    page_icon="🏠",
    layout="wide",
)



def verifier_mot_de_passe() -> bool:
    """Bloque l'accès tant que le mot de passe partagé n'a pas été saisi."""
    if st.session_state.get("authentifie"):
        return True

    try:
        attendu = st.secrets["password"]
    except (KeyError, FileNotFoundError):
        # Diagnostic temporaire : noms des clés vues (jamais les valeurs).
        st.error(
            "Mot de passe non configuré : ajoutez `password` aux secrets. "
            f"Clés détectées : {list(st.secrets.keys())}"
        )
        return False

    _, centre, _ = st.columns([2, 1, 2])
    with centre, st.form("connexion"):
        saisi = st.text_input("Mot de passe", type="password")
        valide = st.form_submit_button("Entrer")

    if valide:
        if hmac.compare_digest(saisi.encode(), str(attendu).encode()):
            st.session_state["authentifie"] = True
            st.rerun()
        st.error("Mot de passe incorrect.")
    return False


accueil = st.Page("views/accueil.py", title="Résidence l'Hermine", icon="🏠", default=True)
annee_2025_26 = st.Page(
    "pages/1_Année_2025_26.py", title="Année 2025-26", icon="📅"
)
ag_2026 = st.Page("pages/1_AG_2026.py", title="AG-2026", icon="🗳️")
journal_2025_26 = st.Page(
    "pages/1_Journal_2025_26.py", title="Journal des interventions", icon="🛠️"
)
ag_2027 = st.Page("pages/2_AG_2027.py", title="AG-2027", icon="🗳️")
vigik_2026_27 = st.Page("pages/2_Vigik_plus.py", title="Vigik+", icon="🔑")
bornes_2026_27 = st.Page(
    "pages/2_Bornes_rechargeables.py", title="Bornes rechargeables", icon="🔌"
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
    (annee_2026_27, [ag_2027, vigik_2026_27, bornes_2026_27, journal_2026_27]),
]

# Le menu natif de Streamlit n'imbrique pas les pages : il est masqué et
# remplacé par des liens, les sous-pages étant décalées vers la droite.
pg = st.navigation(
    pages=[page for parent, enfants in MENU for page in [parent, *enfants]],
    position="hidden",
)

# Navigation déclarée (et masquée) avant le blocage : sinon Streamlit affiche
# son menu automatique pendant la saisie du mot de passe.
if not verifier_mot_de_passe():
    st.stop()

with st.sidebar:
    st.html("<style>[class*='st-key-sous_menu_'] { padding-left: 1.5rem; }</style>")
    for index, (parent, enfants) in enumerate(MENU):
        st.page_link(parent)
        if enfants:
            with st.container(key=f"sous_menu_{index}"):
                for enfant in enfants:
                    st.page_link(enfant)

pg.run()
