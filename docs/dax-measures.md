# Mesures DAX

Les **23 mesures** du modèle, regroupées par thème. Toutes sont rattachées à la table de faits `Ventes`.
Format : `$` = monétaire, `%` = pourcentage, `#` = nombre entier.

## 01 · Finance

### Chiffre d'affaires — `$`
```dax
Chiffre d'affaires = SUM(Ventes[MontantLigne])
```
Total des ventes (toutes taxes exclues).

### Coût matière — `$`
```dax
Coût matière = SUM(Ventes[CoutMatiereLigne])
```
Coût des denrées (*food cost* en dollars).

### Food Cost % — `%`
```dax
Food Cost % = DIVIDE([Coût matière], [Chiffre d'affaires])
```
Ratio coût matière / CA. Cible usuelle en restauration : **28–35 %**.

### Marge brute — `$`
```dax
Marge brute = [Chiffre d'affaires] - [Coût matière]
```

### Marge brute % — `%`
```dax
Marge brute % = DIVIDE([Marge brute], [Chiffre d'affaires])
```

### Coût personnel — `$`
```dax
Coût personnel = SUM(Charges[MainOeuvre])
```
Masse salariale (*labor cost*).

### Labor Cost % — `%`
```dax
Labor Cost % = DIVIDE([Coût personnel], [Chiffre d'affaires])
```
Cible usuelle : **25–35 %**.

### Prime Cost — `$`
```dax
Prime Cost = [Coût matière] + [Coût personnel]
```
Coût matière + main d'œuvre — l'indicateur de rentabilité le plus surveillé en restauration.

### Prime Cost % — `%`
```dax
Prime Cost % = DIVIDE([Prime Cost], [Chiffre d'affaires])
```
Cible usuelle : **≤ 60–65 %**.

### Charges fixes — `$`
```dax
Charges fixes =
    SUM(Charges[Loyer]) + SUM(Charges[Energie])
  + SUM(Charges[Marketing]) + SUM(Charges[Autres])
```

### Gaspillage — `$`
```dax
Gaspillage = SUM(Charges[Gaspillage])
```

### Gaspillage % — `%`
```dax
Gaspillage % = DIVIDE([Gaspillage], [Coût matière])
```
Part du coût matière perdue en gaspillage.

### Résultat net — `$`
```dax
Résultat net = [Marge brute] - [Coût personnel] - [Charges fixes]
```

### Marge nette % — `%`
```dax
Marge nette % = DIVIDE([Résultat net], [Chiffre d'affaires])
```

## 02 · Activité

### Quantité vendue — `#`
```dax
Quantité vendue = SUM(Ventes[Quantite])
```

### Nombre de commandes — `#`
```dax
Nombre de commandes = DISTINCTCOUNT(Ventes[OrderID])
```

### Ticket moyen — `$`
```dax
Ticket moyen = DIVIDE([Chiffre d'affaires], [Nombre de commandes])
```

### CA mois précédent — `$`
```dax
CA mois précédent = CALCULATE([Chiffre d'affaires], DATEADD(Calendrier[Date], -1, MONTH))
```

### Croissance CA % — `%`
```dax
Croissance CA % = DIVIDE([Chiffre d'affaires] - [CA mois précédent], [CA mois précédent])
```

## 03 · Menu

### Nombre de plats — `#`
```dax
Nombre de plats = DISTINCTCOUNT(Menu[MenuItemID])
```

### Marge de contribution — `$`
```dax
Marge de contribution = [Chiffre d'affaires] - [Coût matière]
```
Contribution d'un plat à la couverture des charges fixes.

### Popularité % — `%`
```dax
Popularité % = DIVIDE([Quantité vendue], CALCULATE([Quantité vendue], ALL(Menu)))
```
Part d'un plat dans le volume total vendu.

### Classe menu — `texte`
Classification *menu engineering* : croise la **popularité** (volume vs moyenne) et la **rentabilité** (marge % vs moyenne).
```dax
Classe menu =
VAR MargePct = [Marge brute %]
VAR AvgMarge = CALCULATE([Marge brute %], ALL(Menu))
VAR Qte      = [Quantité vendue]
VAR NbItems  = CALCULATE(DISTINCTCOUNT(Menu[MenuItemID]), ALL(Menu))
VAR TotQte   = CALCULATE([Quantité vendue], ALL(Menu))
VAR AvgQte   = DIVIDE(TotQte, NbItems)
RETURN
IF(ISBLANK(Qte), BLANK(),
    SWITCH(TRUE(),
        Qte >= AvgQte && MargePct >= AvgMarge, "Star",                -- populaire + rentable
        Qte >= AvgQte && MargePct <  AvgMarge, "Cheval de bataille",  -- populaire, marge faible
        Qte <  AvgQte && MargePct >= AvgMarge, "Enigme",              -- rentable, peu vendu
        "Poids mort"))                                                -- peu vendu + faible marge
```

| Classe | Popularité | Marge | Action recommandée |
|---|:---:|:---:|---|
| **Star** | ▲ | ▲ | Mettre en avant, protéger |
| **Cheval de bataille** | ▲ | ▼ | Optimiser le coût / la portion |
| **Énigme** | ▼ | ▲ | Repositionner, promouvoir |
| **Poids mort** | ▼ | ▼ | Retirer ou retravailler |
