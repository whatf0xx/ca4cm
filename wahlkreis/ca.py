"""
Correspondence analysis of the 2024 Vienna Nationalratswahl results
(national elections) by Bezirk (city district). Data pulled from:
https://www.data.gv.at/datasets/b9193b21-6053-4de6-a118-d10380be8648
"""
import matplotlib.pyplot as plt
from pandas import read_csv
from prince import CA


if __name__ == "__main__":
    df = read_csv("wahlkreis/NR241.csv", sep=";", encoding="latin-1")
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    bezirks = df[(df["Typ"] == "Bezirk") & df["Stimmtyp"].isna()]
    to_exclude = [
        "Kurzbezeichnung", "Langbezeichnung", "Timestamp",
        "NUTS1", "NUTS2", "NUTS3",
        "Typ", "Landeswahlkreis", "Wahlkreis",
        "DistrictCode", "Sprengelnummer",
        "Stimmtyp", "ErfassungseinheitTyp",
        "Ungültige Stimmen", "Status",
    ]
    bezirks = bezirks.drop(columns=to_exclude).set_index("Bezirk")
    ct = bezirks.drop(columns=[
                          "Wahlberechtigte",
                          "Abgegebene Stimmen",
                      ])
    
    ca = CA(
        n_components=10,
    )

    ca.fit(ct)
    print(ca.eigenvalues_summary)
    pct1, pct2 = ca.percentage_of_variance_[:2]

    eigs = ca.eigenvalues_[:2]
    # col_coords = ca.column_coordinates(ct).iloc[:, :2] / eigs**0.5
    col_coords = ca.column_coordinates(ct).iloc[:, :2]
    row_coords = ca.row_coordinates(ct).iloc[:, :2]

    # Column points: parties
    # Keys match the latin-1-decoded column names (byte 0x96 = en-dash surrogate)
    party_info = {
        "Karl Nehammer \x96 Die Volkspartei":                              {"abbr": "ÖVP",      "color": "#00B0CC"},
        "Sozialdemokratische Partei Österreichs":                          {"abbr": "SPÖ",      "color": "#E3001B"},
        "Freiheitliche Partei Österreichs":                                {"abbr": "FPÖ",      "color": "#0056A2"},
        "Die Grünen \x96 Die Grüne Alternative":                           {"abbr": "Grüne",    "color": "#80B526"},
        "NEOS \x96 Die Reformkraft für dein neues Österreich":             {"abbr": "NEOS",     "color": "#E84188"},
        "Die Bierpartei":                                                  {"abbr": "Bier",     "color": "#F5A623"},
        "Kommunistische Partei Österreichs \x96 KPÖ Plus":                 {"abbr": "KPÖ+",    "color": "#8B0000"},
        "Liste GAZA \x96 Stimmen gegen den Völkermord":                    {"abbr": "GAZA",     "color": "#556B2F"},
        "Liste Madeleine Petrovic":                                        {"abbr": "Petrovic", "color": "#9B59B6"},
        "MFG \x96 Österreich Menschen \x96 Freiheit \x96 Grundrechte":    {"abbr": "MFG",      "color": "#E67E22"},
        "Keine von denen":                                                 {"abbr": "N/A",      "color": "#7F8C8D"},
    }
    colors  = {k: v["color"] for k, v in party_info.items()}
    abbrevs = {k: v["abbr"]  for k, v in party_info.items()}

    # Row points: Bezirke (Vienna districts 1–23)
    # Muted colors via tab20b/tab20c to avoid clashing with party markers
    _cmap = plt.get_cmap("tab20b", 23)
    bezirk_info = {name: {"number": i + 1, "color": _cmap(i)}
                   for i, name in enumerate([
        "Innere Stadt",        # 1
        "Leopoldstadt",        # 2
        "Landstraße",          # 3
        "Wieden",              # 4
        "Margareten",          # 5
        "Mariahilf",           # 6
        "Neubau",              # 7
        "Josefstadt",          # 8
        "Alsergrund",          # 9
        "Favoriten",           # 10
        "Simmering",           # 11
        "Meidling",            # 12
        "Hietzing",            # 13
        "Penzing",             # 14
        "Rudolfsheim-Fünfhaus",# 15
        "Ottakring",           # 16
        "Hernals",             # 17
        "Währing",             # 18
        "Döbling",             # 19
        "Brigittenau",         # 20
        "Floridsdorf",         # 21
        "Donaustadt",          # 22
        "Liesing",             # 23
    ])}
    bezirk_colors = {k: v["color"] for k, v in bezirk_info.items()}
    bezirk_nums   = {k: v["number"] for k, v in bezirk_info.items()}

    plt.figure()
    plt.xlabel(f"Dimension 1 ({pct1:.1f}% inertia)")
    plt.ylabel(f"Dimension 2 ({pct2:.1f}% inertia)")

    for label, coords in col_coords.iterrows():
        plt.scatter(*coords, color=colors[label], marker="D", s=60, zorder=5)
        plt.text(*(coords+ [0.01, 0.005]), abbrevs[label], color=colors[label], fontsize=9)

    for label, coords in row_coords.iterrows():
        plt.scatter(
                *coords,
                color=bezirk_info[label]["color"],
                alpha=0.8,
                s=60,
                zorder=5,
            )
        plt.text(
                *(coords+ [0.01, 0.005]),
                f"{label} ({bezirk_info[label]['number']})",
                color=bezirk_info[label]["color"],
                fontsize=9,
            )

    plt.axhline(0, lw=0.8, color="gray")
    plt.axvline(0, lw=0.8, color="gray")

    plt.show()
