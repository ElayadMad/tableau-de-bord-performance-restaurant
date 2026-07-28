# 🍽️ Tableau de Bord — Performance Restaurant (Power BI)

> Tableau de bord décisionnel **Power BI** conçu pour les **restaurateurs indépendants** : suivi des KPI financiers (food cost, prime cost, marge nette) et analyse du menu (*menu engineering*), à partir des données de caisse.

<p align="left">
  <img alt="Power BI"  src="https://img.shields.io/badge/Power_BI-F2C811?logo=powerbi&logoColor=282828&style=flat-square">
  <img alt="DAX"       src="https://img.shields.io/badge/DAX-23_mesures-6d4b3e?style=flat-square">
  <img alt="Python"    src="https://img.shields.io/badge/Python-Génération_données-3776AB?logo=python&logoColor=white&style=flat-square">
  <img alt="Licence"   src="https://img.shields.io/badge/Licence-MIT-a9afa9?style=flat-square">
</p>

**Projet réalisé pour [Maison Madihali](#-contexte) — maison de conseil en restauration & performance.**
Données **fictives mais réalistes** (~80 000 lignes de ventes sur 12 mois, ≈ 1,1 M$ de chiffre d'affaires), générées par script pour la démonstration.

---

## 📸 Aperçu

| Vue d'ensemble | Finance & Rentabilité | Menu Engineering |
|:---:|:---:|:---:|
| ![Vue d'ensemble](assets/screenshots/01-vue-ensemble.pdf) | ![Finance](assets/screenshots/02-finance.pdf) | ![Menu](assets/screenshots/03-menu-engineering.pdf) |


---

## 🎯 Contexte

**Maison Madihali** accompagne les restaurateurs indépendants aux marges serrées. Le livrable phare est un **tableau de bord de KPI vitaux** (food cost, gaspillage, marge) mis à jour mensuellement. Ce dépôt reproduit ce livrable de bout en bout :

- un **modèle de données en étoile** (1 table de faits + 3 dimensions) ;
- **23 mesures DAX** couvrant la rentabilité et l'ingénierie de menu ;
- un **rapport 3 pages** aux couleurs de la marque (palette terreuse).

## 📊 Le rapport (3 pages)

### 1. Vue d'ensemble
KPI clés (CA, résultat net, marge nette %, food cost %, ticket moyen), évolution mensuelle CA & marge, répartition du CA par catégorie, par canal de vente et par jour de la semaine, synthèse mensuelle.

### 2. Finance & Rentabilité
Décomposition des coûts, **prime cost**, ratios de gestion (food cost, labor cost, gaspillage), **compte de résultat mensuel (P&L)**, jauge de marge nette.

### 3. Menu Engineering
Matrice **Popularité × Marge** (taille = CA), classification de chaque plat en **Star · Cheval de bataille · Énigme · Poids mort**, mix des ventes et marge par catégorie, tableau détaillé des plats.

## 🧠 KPI & indicateurs suivis

| Financier | Menu / Activité |
|---|---|
| Chiffre d'affaires · Coût matière | Quantité vendue · Nombre de commandes |
| **Food Cost %** · Marge brute % | Ticket moyen · Nombre de plats |
| Coût personnel · **Labor Cost %** | **Popularité %** · Marge de contribution |
| **Prime Cost** ($ et %) | **Classe menu** (Star / Cheval / Énigme / Poids mort) |
| Charges fixes · Gaspillage % | Croissance CA (vs mois précédent) |
| **Résultat net** · **Marge nette %** | |

➡️ Formules complètes : [`docs/dax-measures.md`](docs/dax-measures.md) · Définitions métier : [`docs/kpi-glossary.md`](docs/kpi-glossary.md)

## 🗂️ Modèle de données

Schéma en étoile — table de faits `Ventes` reliée à trois dimensions :

```
        ┌──────────────┐        ┌──────────────┐
        │     Menu     │        │  Calendrier  │
        │  (40 plats)  │        │  (365 jours) │
        └──────┬───────┘        └──────┬───────┘
               │ 1                     │ 1
               │                       │
               ▼ *                     ▼ *
            ┌─────────────────────────────┐        ┌──────────────┐
            │           Ventes            │        │   Charges    │
            │   (~80 000 lignes / faits)  │        │ (12 mois)    │
            └─────────────────────────────┘        └──────┬───────┘
                                       Calendrier ────────┘ (via AnneeMois)
```

Détail des tables, colonnes et relations : [`docs/data-model.md`](docs/data-model.md) · Dictionnaire de données : [`docs/data-dictionary.md`](docs/data-dictionary.md)

## 📁 Structure du dépôt

```
restaurant-performance-dashboard/
├── Tableau-de-Bord-Restaurant.pbix   # Le rapport Power BI (données en cache)
├── data/                             # Données sources (CSV)
│   ├── ventes.csv                    #   Faits — lignes de commande
│   ├── menu.csv                      #   Dimension — carte / plats
│   ├── calendrier.csv                #   Dimension — table de dates
│   └── charges.csv                   #   Dimension — charges mensuelles
├── scripts/
│   └── generate_data.py              # Génère les CSV (données fictives, reproductible)
├── docs/
│   ├── data-model.md                 # Tables, colonnes, relations
│   ├── data-dictionary.md            # Dictionnaire de données détaillé
│   ├── dax-measures.md               # Les 23 mesures DAX + formules
│   └── kpi-glossary.md               # Définitions métier des KPI
├── assets/screenshots/               # Captures du rapport
├── requirements.txt
├── LICENSE
└── README.md
```

## 🚀 Utilisation

**Consulter le rapport**
1. Installer **[Power BI Desktop](https://www.microsoft.com/fr-fr/download/details.aspx?id=58494)** (gratuit).
2. Ouvrir `Tableau-de-Bord-Restaurant.pbix`. Les données sont en cache — le rapport s'affiche immédiatement.

**Régénérer les données (optionnel)**
```bash
python scripts/generate_data.py      # réécrit les 4 CSV dans data/
```
> Pour actualiser dans Power BI après régénération : *Accueil ▸ Transformer les données ▸ Paramètres de la source* et pointer vers votre dossier `data/` local, puis *Actualiser*.

## 🛠️ Stack technique

- **Power BI Desktop** — modélisation, DAX, visualisations
- **DAX** — 23 mesures (rentabilité + menu engineering)
- **Power Query (M)** — import et typage des CSV
- **Python** (bibliothèque standard) — génération des données de démonstration

## 📌 À noter

- Les données sont **entièrement fictives** (générées avec une graine aléatoire fixe → reproductibles). Aucune donnée réelle de client.
- Le `.pbix` embarque les données en cache ; les chemins de source pointent vers un dossier local et doivent être ré-adressés pour une actualisation.

## 📄 Licence

Distribué sous licence **MIT** — voir [`LICENSE`](LICENSE).

---

<p align="center"><sub>Maison Madihali · Conseil en restauration & performance · Données de démonstration</sub></p>
