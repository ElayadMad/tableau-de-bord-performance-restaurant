# -*- coding: utf-8 -*-
import csv, os, random, datetime
random.seed(42)

# Écrit les CSV dans ../data (relatif à l'emplacement du script) — portable après un git clone.
DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA, exist_ok=True)

# ---------------------------------------------------------------- MENU
# (nom, categorie, prix, food_cost_ratio, popularite_poids)
menu_src = [
    # Entrees
    ("Soupe du jour",              "Entrees", 7.50, 0.24, 55),
    ("Salade Maison",             "Entrees", 11.00, 0.30, 80),
    ("Salade de chevre chaud",    "Entrees", 13.50, 0.33, 70),
    ("Bruschetta tomates",        "Entrees", 9.50, 0.28, 45),
    ("Assiette de charcuterie",   "Entrees", 15.00, 0.38, 60),
    ("Croquettes de fromage",     "Entrees", 10.50, 0.31, 50),
    ("Tartare de saumon",         "Entrees", 16.50, 0.40, 40),
    ("Foie gras maison",          "Entrees", 21.00, 0.45, 22),
    # Plats
    ("Burger Maison",             "Plats", 18.50, 0.34, 160),
    ("Entrecote grillee",         "Plats", 29.00, 0.42, 95),
    ("Filet de saumon",           "Plats", 26.00, 0.40, 85),
    ("Risotto aux champignons",   "Plats", 21.00, 0.28, 70),
    ("Pates carbonara",           "Plats", 17.50, 0.26, 120),
    ("Magret de canard",          "Plats", 27.50, 0.41, 65),
    ("Poulet roti & frites",      "Plats", 19.50, 0.32, 110),
    ("Curry de legumes",          "Plats", 18.00, 0.25, 48),
    ("Fish & chips",              "Plats", 20.00, 0.36, 72),
    ("Cassoulet maison",          "Plats", 22.50, 0.35, 40),
    ("Pizza Regina",              "Plats", 16.00, 0.27, 90),
    ("Lasagnes bolognaise",       "Plats", 18.00, 0.30, 88),
    # Accompagnements
    ("Frites maison",             "Accompagnements", 5.50, 0.22, 140),
    ("Legumes de saison",         "Accompagnements", 6.00, 0.28, 55),
    ("Gratin dauphinois",         "Accompagnements", 6.50, 0.26, 60),
    ("Salade verte",              "Accompagnements", 4.50, 0.20, 65),
    # Desserts
    ("Creme brulee",              "Desserts", 8.50, 0.22, 130),
    ("Fondant au chocolat",       "Desserts", 9.00, 0.26, 125),
    ("Tarte Tatin",               "Desserts", 8.50, 0.25, 75),
    ("Tiramisu",                  "Desserts", 8.00, 0.24, 95),
    ("Cheesecake",                "Desserts", 8.50, 0.27, 68),
    ("Assiette de fromages",      "Desserts", 11.00, 0.40, 35),
    ("Cafe gourmand",             "Desserts", 9.50, 0.23, 88),
    ("Glace 2 boules",            "Desserts", 6.00, 0.28, 60),
    # Boissons
    ("Verre de vin rouge",        "Boissons", 6.50, 0.20, 150),
    ("Verre de vin blanc",        "Boissons", 6.50, 0.20, 110),
    ("Biere pression",            "Boissons", 6.00, 0.18, 135),
    ("Cocktail maison",           "Boissons", 11.00, 0.22, 80),
    ("Eau minerale",              "Boissons", 4.00, 0.12, 160),
    ("Soda",                      "Boissons", 4.50, 0.15, 120),
    ("Cafe / The",               "Boissons", 3.00, 0.10, 175),
    ("Jus de fruits frais",       "Boissons", 5.50, 0.30, 70),
]

menu = []
for i, (nom, cat, prix, fcr, poids) in enumerate(menu_src, start=1):
    cout = round(prix * fcr, 2)
    menu.append({
        "MenuItemID": i, "NomPlat": nom, "Categorie": cat,
        "PrixMenu": prix, "CoutMatiereUnitaire": cout,
        "MargeUnitaire": round(prix - cout, 2), "_poids": poids
    })

with open(os.path.join(DATA, "menu.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["MenuItemID", "NomPlat", "Categorie", "PrixMenu", "CoutMatiereUnitaire", "MargeUnitaire"])
    for m in menu:
        w.writerow([m["MenuItemID"], m["NomPlat"], m["Categorie"], m["PrixMenu"],
                    m["CoutMatiereUnitaire"], m["MargeUnitaire"]])

# ---------------------------------------------------------------- CALENDRIER
mois_noms = ["Janvier","Fevrier","Mars","Avril","Mai","Juin","Juillet",
             "Aout","Septembre","Octobre","Novembre","Decembre"]
jours_noms = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
start = datetime.date(2025, 7, 1)
end = datetime.date(2026, 6, 30)
dates = []
d = start
while d <= end:
    dates.append(d)
    d += datetime.timedelta(days=1)

with open(os.path.join(DATA, "calendrier.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Date","Annee","MoisNum","MoisNom","AnneeMois","Trimestre",
                "Jour","JourSemaineNum","JourSemaineNom","EstWeekend"])
    for dt in dates:
        wd = dt.weekday()
        w.writerow([dt.isoformat(), dt.year, dt.month, mois_noms[dt.month-1],
                    f"{dt.year}-{dt.month:02d}", f"T{(dt.month-1)//3+1}",
                    dt.day, wd+1, jours_noms[wd], 1 if wd >= 5 else 0])

# ---------------------------------------------------------------- VENTES (fact)
canaux = [("Sur place", 0.62), ("A emporter", 0.22), ("Livraison", 0.16)]
def pick_canal():
    r = random.random(); c = 0
    for name, p in canaux:
        c += p
        if r <= c: return name
    return "Sur place"

# seasonality multiplier by month number
season = {1:0.85,2:0.88,3:0.95,4:1.0,5:1.08,6:1.12,7:1.15,8:1.05,
          9:1.0,10:0.98,11:0.95,12:1.20}

weights = [m["_poids"] for m in menu]
order_id = 0
rows = []
for dt in dates:
    wd = dt.weekday()
    base = 55 if wd < 4 else (85 if wd < 6 else 70)  # covers/day pattern
    base *= season[dt.month]
    # growth trend across the year (~ +12%)
    day_index = (dt - start).days
    base *= (1 + 0.12 * day_index / 365.0)
    n_orders = max(5, int(random.gauss(base, base*0.15)))
    for _ in range(n_orders):
        order_id += 1
        service = "Midi" if random.random() < 0.42 else "Soir"
        canal = pick_canal()
        n_items = random.choices([1,2,3,4,5,6], weights=[10,26,28,20,11,5])[0]
        chosen = random.choices(menu, weights=weights, k=n_items)
        # ensure a drink often present in soir
        for m in chosen:
            qte = random.choices([1,2,3], weights=[80,17,3])[0]
            montant = round(m["PrixMenu"] * qte, 2)
            cout = round(m["CoutMatiereUnitaire"] * qte, 2)
            rows.append([order_id, dt.isoformat(), service, canal,
                         m["MenuItemID"], qte, m["PrixMenu"], montant, cout])

with open(os.path.join(DATA, "ventes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["OrderID","Date","Service","Canal","MenuItemID","Quantite",
                "PrixUnitaire","MontantLigne","CoutMatiereLigne"])
    w.writerows(rows)

# ---------------------------------------------------------------- CHARGES (monthly)
# aggregate revenue & food cost per month to scale charges realistically
from collections import defaultdict
rev = defaultdict(float); fc = defaultdict(float)
menu_by_id = {m["MenuItemID"]: m for m in menu}
for r in rows:
    ym = r[1][:7]
    rev[ym] += r[7]; fc[ym] += r[8]

with open(os.path.join(DATA, "charges.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["AnneeMois","MainOeuvre","Loyer","Energie","Marketing","Autres","Gaspillage"])
    for ym in sorted(rev):
        r = rev[ym]
        mo = round(r * random.uniform(0.30, 0.335), 2)      # labor ~30-33% of revenue
        loyer = 4200.0
        energie = round(random.uniform(1300, 1750), 2)
        marketing = round(r * random.uniform(0.018, 0.03), 2)
        autres = round(random.uniform(1600, 2200), 2)
        gaspillage = round(fc[ym] * random.uniform(0.04, 0.075), 2)  # % of food cost
        w.writerow([ym, mo, loyer, energie, marketing, autres, gaspillage])

print("Menu items:", len(menu))
print("Fact rows :", len(rows))
print("Orders    :", order_id)
print("Total CA  :", round(sum(r[7] for r in rows), 2))
print("Data dir  :", DATA)
