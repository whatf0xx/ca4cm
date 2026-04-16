import matplotlib.pyplot as plt
import pandas as pd
from prince import MCA


if __name__ == "__main__":
    df = pd.read_csv("taste/data.csv")
    df = df[df["Isup"] == "Active"]            # filters out the excluded participants
    active_cols = ["TV", "Film", "Art", "Eat"]
    active = df[active_cols]                   # active columns for the MCA
    cats = sum(active.nunique().values)        # total no. of categories in data
               

    mca = MCA(
        n_components = cats - len(active_cols),  # categories - no. of variables
        correction = "benzecri",
    )

    mca.fit(active)
    print(summary := mca.eigenvalues_summary.iloc[:3])
    pct1, pct2 = mca.percentage_of_variance_[:2]

    column_coords = mca.column_coordinates(active)[[0, 1]]

    _parts = column_coords.index.to_series().str.split("__", expand=True)
    column_coords.index = _parts[1]
    column_coords["variable"] = _parts[0].values

    # now we want to calculate the "supplementary point" by projecting these columns into the space as averages of the row profiles that comprise them
    print("Age categories: ", list(df["Age"].unique()))
    print("Income categories: ", list(df["Income"].unique()))
    row_coords = mca.row_coordinates(active)
    # print(row_coords.head())
    # print(row_coords.mean(axis=0))  # should be 0 because average row is at the origin
    age_cats = [
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55-64",
        "65+",
    ]
    inc_cats = [
        "GBP: <9",
        "GBP: 10-19",
        "GBP: 20-29",
        "GBP: 30-39",
        "GBP: 40-59",
        "GBP: >=60", 
    ]
    ages = {age_cat: [] for age_cat in age_cats}
    incs = {inc_cat: [] for inc_cat in inc_cats}
    for index, row in df.iterrows():
        ages[row["Age"]].append(index)
        if isinstance(row["Income"], str):
            incs[row["Income"]].append(index)

    age_supp = {
        k: row_coords.iloc[v].mean(axis=0)[[0, 1]] for k, v in ages.items() 
    }
    inc_supp = {
        k: row_coords.iloc[v].mean(axis=0)[[0, 1]] for k, v in incs.items() 
    }
    
    fig, ax = plt.subplots(figsize=(8, 5), layout="constrained")
    colors = {
        "TV":   "#3863D1",
        "Film": "#D138B0",
        "Art":  "#D1A638",
        "Eat":  "#38D159",
    }
    for col in active_cols:
        pts = column_coords[column_coords["variable"] == col]
        x, y = pts[0], pts[1]
        ax.scatter(x, y, color=colors[col], label=col)
        for label, xi, yi in zip(pts.index, x, y):
            if col == "TV":
                label = label.split("-")[1]
            ax.annotate(
                    label,
                    (xi, yi),
                    textcoords="offset points",
                    xytext=(5, 5),
                    fontsize=9,
                    color=colors[col]
                )

    ax.legend()
    ax.axvline(0, color="k", alpha=0.8, linewidth=0.8, zorder=0)
    ax.axhline(0, color="k", alpha=0.8, linewidth=0.8, zorder=0)
    ax.set_ylabel(f"Dimension 2 ({pct2:.1f}% variance)")
    ax.set_xlabel(f"Dimension 1 ({pct1:.1f}% variance)")
    fig.savefig("active_taste_cols.pdf", transparent=True)
    fig1, ax = plt.subplots(figsize=(8, 5), layout="constrained")
    ax.axvline(0, color="k", alpha=0.8, linewidth=0.8, zorder=0)
    ax.axhline(0, color="k", alpha=0.8, linewidth=0.8, zorder=0)
    ax.set_ylabel(f"Dimension 2 ({pct2:.1f}% variance)")
    ax.set_xlabel(f"Dimension 1 ({pct1:.1f}% variance)")
    ax.set_xlim(-0.6, 0.6)
    ax.set_ylim(-0.5, 0.5)
    for col in active_cols:
        pts = column_coords[column_coords["variable"] == col]
        x, y = pts[0], pts[1]
        ax.scatter(x, y, color=colors[col], label=col)
    age_pts = [a.to_numpy() for a in age_supp.values()]
    ax.plot(*zip(*age_pts),
            marker="o",
            linestyle="dashed",
            color="gray",
            label="Age (supp.)")
    for cat, coords in age_supp.items():
        ax.annotate(
                cat,
                coords.to_numpy(),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=9,
                color="gray"
            )

    inc_pts = [a.to_numpy() for a in inc_supp.values()]
    ax.plot(*zip(*inc_pts),
            marker="s",
            linestyle="dashed",
            color="brown",
            label="Income (supp.)")
    for cat, coords in inc_supp.items():
        ax.annotate(
                cat,
                coords.to_numpy(),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=9,
                color="brown"
            )

    ax.legend()
    fig1.savefig("supp_taste_cols.pdf", transparent=True)
    plt.show()
