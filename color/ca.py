import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import combinations
from mpl_toolkits.mplot3d import Axes3D
from prince import CA


if __name__ == "__main__":
    ct = pd.read_csv("color/data.csv", index_col=0)
    ca = CA(n_components=3)  # min(rows - 1, columns - 1)
    ca.fit(ct)

    print("Total inertia in the table: ", ca.total_inertia_)
    print(summary := ca.eigenvalues_summary)
    pct1 = summary["% of variance"].iloc[0]
    pct2 = summary["% of variance"].iloc[1]
    pct3 = summary["% of variance"].iloc[2]

    eigs = ca.eigenvalues_
    row_coords = ca.row_coordinates(ct)                              # rows in principal coordinates
    col_coords = ca.column_coordinates(ct) / eigs**0.5    # cols in standard coordinates

    colors = {
        "Brown": "brown",
        "Blue":  "#1772E8",
        "Hazel": "#949200",
        "Green": "#4C9400",
        "Black": "k",
        "Red":   "#940200",
        "Blond": "#F5CC36",
    }
    fig3d = plt.figure(layout="constrained")
    ax3d = fig3d.add_subplot(111, projection="3d")

    for label, col in col_coords.iterrows():
        ax3d.scatter(*col, color=colors[label], marker="D", s=60, zorder=5)
        ax3d.text(*col, f"  {label}", color=colors[label], fontsize=9)

    # Connect every pair of vertices with thin dark grey lines
    for (l1, (x1, y1, z1)), (l2, (x2, y2, z2)) in combinations(col_coords.iterrows(), 2):
        ax3d.plot([x1, x2], [y1, y2], [z1, z2], color="#333333", linewidth=0.8, zorder=1)

    # Row points inside the tetrahedron
    for label, row in row_coords.iterrows():
        x, y, z = row
        ax3d.scatter(*row, color=colors[label], s=60, zorder=5)
        ax3d.text(*row, f"  {label}", color=colors[label], fontsize=9)

    ax3d.set_xlabel(f"Dim 1 ({pct1} variance)")
    ax3d.set_ylabel(f"Dim 2 ({pct2} variance)")
    ax3d.set_zlabel(f"Dim 3 ({pct3} variance)")
    fig3d.savefig("3d_proj.pdf", bbox_inches="tight")

    fig, ax = plt.subplots(layout="constrained")
    
    dim3_vals = [col[2] for _, col in col_coords.iterrows()]
    var3 = np.var(dim3_vals)
    def _alpha(z):
        return float(np.exp(-z**2 / (2 * var3)))

    for label, col in col_coords.iterrows():
        ax.scatter(*col.iloc[:2], color=colors[label], marker="D", s=60, zorder=5, alpha=_alpha(col[2]))
        ax.text(*col.iloc[:2], f"  {label}", color=colors[label], fontsize=9, alpha=_alpha(col[2]))

    # Connect every pair of vertices with thin dark grey lines
    for (l1, (x1, y1, z1)), (l2, (x2, y2, z2)) in combinations(col_coords.iterrows(), 2):
        ax.plot([x1, x2], [y1, y2], color="#333333", linewidth=0.8, zorder=1,
                alpha=min(_alpha(z1), _alpha(z2)))

    # Row points inside the tetrahedron
    for label, row in row_coords.iterrows():
        x, y, z = row
        ax.scatter(*row.iloc[:2], color=colors[label], s=60, zorder=5)
        ax.text(*row.iloc[:2], f"  {label}", color=colors[label], fontsize=9)

    ax.set_xlabel(f"Dim 1 ({pct1} variance)")
    ax.set_ylabel(f"Dim 2 ({pct2} variance)")
    

    plt.show()
