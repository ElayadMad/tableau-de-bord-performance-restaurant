# Modèle de données

Schéma **en étoile** : une table de faits (`Ventes`) entourée de trois dimensions
(`Menu`, `Calendrier`, `Charges`). Import en mémoire (VertiPaq), source = fichiers CSV.

## Diagramme relationnel

```
                    ┌───────────────────────┐
                    │       Calendrier      │
                    │  Date (PK)            │
                    │  MoisNom · Trimestre  │
                    │  JourSemaineNom · …   │
                    └───────┬───────────────┘
                            │ 1        │ 1 (AnneeMois)
                            │          └──────────────┐
                            ▼ *                        ▼ *  (bidirectionnelle)
   ┌───────────────┐   ┌──────────────────────┐   ┌───────────────────┐
   │     Menu      │ 1 │        Ventes         │   │      Charges      │
   │ MenuItemID PK │──▶│  (table de faits)     │   │  AnneeMois (PK)   │
   │ NomPlat · …   │ * │  Date · MenuItemID …  │   │  MainOeuvre · …   │
   └───────────────┘   └──────────────────────┘   └───────────────────┘
```

## Relations

| De (côté plusieurs `*`) | Vers (côté un `1`) | Cardinalité | Filtre | Rôle |
|---|---|:---:|---|---|
| `Ventes[MenuItemID]` | `Menu[MenuItemID]` | * : 1 | Simple (Menu → Ventes) | Rattache chaque ligne au plat |
| `Ventes[Date]` | `Calendrier[Date]` | * : 1 | Simple (Calendrier → Ventes) | Axe temporel + time intelligence |
| `Calendrier[AnneeMois]` | `Charges[AnneeMois]` | * : 1 | **Bidirectionnelle** | Croiser charges mensuelles et ventes |

> La relation **bidirectionnelle** `Calendrier ↔ Charges` permet aux mesures de charges
> (coût personnel, charges fixes) de réagir aux filtres de période appliqués via `Calendrier`.

## Tables

### `Ventes` — table de faits (~80 000 lignes)
Une ligne = un article vendu au sein d'une commande.

| Colonne | Type | Description |
|---|---|---|
| `OrderID` | Entier | Identifiant de commande (une commande = plusieurs lignes) |
| `Date` | Date | Date de la vente → relié à `Calendrier` |
| `Service` | Texte | `Midi` / `Soir` |
| `Canal` | Texte | `Sur place` / `A emporter` / `Livraison` |
| `MenuItemID` | Entier | Clé étrangère → `Menu` |
| `Quantite` | Entier | Quantité vendue |
| `PrixUnitaire` | Décimal | Prix unitaire ($) |
| `MontantLigne` | Décimal | `PrixUnitaire × Quantite` ($) |
| `CoutMatiereLigne` | Décimal | Coût matière de la ligne ($) |

### `Menu` — dimension (40 plats)
| Colonne | Type | Description |
|---|---|---|
| `MenuItemID` | Entier | Clé primaire |
| `NomPlat` | Texte | Nom du plat |
| `Categorie` | Texte | Entrées · Plats · Accompagnements · Desserts · Boissons |
| `PrixMenu` | Décimal | Prix de vente à la carte ($) |
| `CoutMatiereUnitaire` | Décimal | Coût matière unitaire ($) |
| `MargeUnitaire` | Décimal | `PrixMenu − CoutMatiereUnitaire` ($) |

### `Calendrier` — dimension de dates (365 jours)
Table de dates continue (1 juil. 2025 → 30 juin 2026). `MoisNom` est trié par `MoisNum`,
`JourSemaineNom` par `JourSemaineNum` (ordre chronologique dans les visuels).

| Colonne | Type | Description |
|---|---|---|
| `Date` | Date | Clé primaire |
| `Annee` | Entier | Année |
| `MoisNum` | Entier | 1–12 (colonne de tri de `MoisNom`) |
| `MoisNom` | Texte | Janvier … Décembre |
| `AnneeMois` | Texte | `AAAA-MM` → relié à `Charges` |
| `Trimestre` | Texte | T1–T4 |
| `Jour` | Entier | Jour du mois |
| `JourSemaineNum` | Entier | 1 (Lundi) – 7 (Dimanche) |
| `JourSemaineNom` | Texte | Lundi … Dimanche |
| `EstWeekend` | Entier | 1 si samedi/dimanche, sinon 0 |

### `Charges` — dimension mensuelle (12 lignes)
| Colonne | Type | Description |
|---|---|---|
| `AnneeMois` | Texte | Clé primaire (`AAAA-MM`) |
| `MainOeuvre` | Décimal | Masse salariale du mois ($) |
| `Loyer` | Décimal | Loyer ($) |
| `Energie` | Décimal | Énergie ($) |
| `Marketing` | Décimal | Marketing ($) |
| `Autres` | Décimal | Autres charges ($) |
| `Gaspillage` | Décimal | Coût du gaspillage ($) |

## Choix de modélisation

- **Schéma en étoile** pour des performances optimales et des mesures lisibles.
- **Charges au grain mensuel** (et non par commande) : reflète la réalité comptable d'un
  petit établissement ; croisées avec les ventes via `Calendrier[AnneeMois]`.
- **Time intelligence** via une vraie table `Calendrier` continue (mesures `CA mois précédent`,
  `Croissance CA %`).
