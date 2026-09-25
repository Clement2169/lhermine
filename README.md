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
├── app.py                    # Point d'entrée : navigation (L'Hermine / Année 2025-26)
├── views/
│   └── accueil.py            # Page d'accueil : Résidence l'Hermine
├── pages/
│   └── 1_Année_2025_26.py    # Page Année 2025-26 (5 onglets)
├── pyproject.toml
└── README.md
```
