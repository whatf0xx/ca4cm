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
        n_components = cats - 4,               # categories - no. of variables
        correction = "benzecri",
    )

    mca.fit(active)
    print(summary := mca.eigenvalues_summary)
    pct1 = summary["% of variance"].iloc[0]
    pct2 = summary["% of variance"].iloc[1]
    pct3 = summary["% of variance"].iloc[2]


    column_coords = mca.column_coordinates(active)[[0, 1, 2]]

    _parts = column_coords.index.to_series().str.split("__", expand=True)
    column_coords.index = _parts[1]
    column_coords["variable"] = _parts[0].values
    print(column_coords.head())
    
    fig, axs = plt.subplots(1, 2)
    colors = {
        "TV":   "#3863D1",
        "Film": "#D138B0",
        "Art":  "#D1A638",
        "Eat":  "#38D159",
    }
    for i, ax in enumerate(axs):
        for col in active_cols:
            pts = column_coords[column_coords["variable"] == col]
            x, y = pts[0], pts[i+1]
            ax.scatter(x, y, color=colors[col], label=col if i == 0 else None)
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

        if i == 0:
            ax.legend()
        ax.axvline(0, color="k", alpha=0.8, linewidth=0.8, zorder=0)
        ax.axhline(0, color="k", alpha=0.8, linewidth=0.8, zorder=0)
        if i == 1:
            ax.set_ylabel(f"Dimension 3 ({pct3} variance)")
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
        else:
            ax.set_ylabel(f"Dimension 2 ({pct2} variance)")
            

    fig.supxlabel(f"Dimension 1 ({pct1} variance)")

    plt.show()
