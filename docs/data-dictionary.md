# Dictionnaire de données (fichiers CSV)

Les données sources vivent dans [`../data/`](../data). Encodage **UTF-8**, séparateur **virgule**,
séparateur décimal **point** (`.`), en-têtes en première ligne.

| Fichier | Lignes | Grain | Rôle |
|---|---:|---|---|
| `ventes.csv` | ~80 000 | 1 article vendu / commande | Table de faits |
| `menu.csv` | 40 | 1 plat | Dimension |
| `calendrier.csv` | 365 | 1 jour | Dimension (dates) |
| `charges.csv` | 12 | 1 mois | Dimension (charges) |

---

## `ventes.csv`
| Champ | Type | Domaine / exemple |
|---|---|---|
| `OrderID` | int | 1 … ~25 700 |
| `Date` | date (AAAA-MM-JJ) | 2025-07-01 … 2026-06-30 |
| `Service` | texte | `Midi`, `Soir` |
| `Canal` | texte | `Sur place`, `A emporter`, `Livraison` |
| `MenuItemID` | int | 1 … 40 (→ `menu.csv`) |
| `Quantite` | int | 1 – 3 |
| `PrixUnitaire` | décimal | ex. `18.5` |
| `MontantLigne` | décimal | `PrixUnitaire × Quantite` |
| `CoutMatiereLigne` | décimal | coût matière de la ligne |

```csv
OrderID,Date,Service,Canal,MenuItemID,Quantite,PrixUnitaire,MontantLigne,CoutMatiereLigne
1,2025-07-01,Soir,Sur place,9,1,18.5,18.5,6.29
```

## `menu.csv`
| Champ | Type | Domaine / exemple |
|---|---|---|
| `MenuItemID` | int | 1 … 40 |
| `NomPlat` | texte | ex. `Burger Maison` |
| `Categorie` | texte | `Entrees`, `Plats`, `Accompagnements`, `Desserts`, `Boissons` |
| `PrixMenu` | décimal | prix à la carte |
| `CoutMatiereUnitaire` | décimal | coût matière unitaire |
| `MargeUnitaire` | décimal | `PrixMenu − CoutMatiereUnitaire` |

```csv
MenuItemID,NomPlat,Categorie,PrixMenu,CoutMatiereUnitaire,MargeUnitaire
9,Burger Maison,Plats,18.5,6.29,12.21
```

## `calendrier.csv`
| Champ | Type | Domaine / exemple |
|---|---|---|
| `Date` | date | 2025-07-01 … 2026-06-30 |
| `Annee` | int | 2025, 2026 |
| `MoisNum` | int | 1 – 12 |
| `MoisNom` | texte | `Janvier` … `Decembre` |
| `AnneeMois` | texte | `2025-07` (→ `charges.csv`) |
| `Trimestre` | texte | `T1` – `T4` |
| `Jour` | int | 1 – 31 |
| `JourSemaineNum` | int | 1 (Lundi) – 7 (Dimanche) |
| `JourSemaineNom` | texte | `Lundi` … `Dimanche` |
| `EstWeekend` | int | 0 / 1 |

## `charges.csv`
| Champ | Type | Domaine / exemple |
|---|---|---|
| `AnneeMois` | texte | `2025-07` |
| `MainOeuvre` | décimal | ~30–33 % du CA mensuel |
| `Loyer` | décimal | fixe (4 200) |
| `Energie` | décimal | ~1 300–1 750 |
| `Marketing` | décimal | ~1,8–3 % du CA |
| `Autres` | décimal | ~1 600–2 200 |
| `Gaspillage` | décimal | ~4–7,5 % du coût matière |

```csv
AnneeMois,MainOeuvre,Loyer,Energie,Marketing,Autres,Gaspillage
2025-07,32150.4,4200.0,1523.8,2410.55,1875.3,1204.7
```

---

### Reproductibilité
Les fichiers sont produits par [`../scripts/generate_data.py`](../scripts/generate_data.py) avec une
**graine aléatoire fixe** (`random.seed(42)`) : la régénération donne exactement les mêmes données.
