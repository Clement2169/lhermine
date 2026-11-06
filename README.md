# Résidence l'Hermine

Petit site web Streamlit — Python 3.13.5 + Poetry.

## Prérequis

- Python 3.13.5
- [Poetry](https://python-poetry.org/) >= 2.0

## Installation

```bash
poetry install
```

## Lancement

```bash
poetry run streamlit run app.py
```

Le site est ensuite accessible sur http://localhost:8501

## Structure

```
.
├── app.py                    # Point d'entrée : navigation (Résidence l'Hermine / années)
├── views/
│   ├── accueil.py            # Page d'accueil : Résidence l'Hermine
│   └── annee.py              # Contenu commun des pages d'année (6 onglets)
├── pages/
│   ├── 1_Année_2025_26.py    # Page Année 2025-26
│   └── 2_Année_2026_27.py    # Page Année 2026-27
├── pyproject.toml
└── README.md
```
