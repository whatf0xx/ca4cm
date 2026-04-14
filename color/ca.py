import matplotlib.pyplot as plt
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
    for label, row in row_coords.iterrows():
        x, y = row.iloc[0], row.iloc[1]
        plt.scatter(x, y, color=colors[label])
        plt.annotate(
                label,
                (x, y),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=9,
                color=colors[label]
            )

    for label, col in col_coords.iterrows():
        x, y = col.iloc[0], col.iloc[1]
        plt.scatter(col.iloc[0], col.iloc[1], color=colors[label], marker="D")
        plt.annotate(
                label,
                (x, y),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=9,
                color=colors[label]
            )

    plt.xlabel(f"Dimension 1 ({pct1} variance)")
    plt.ylabel(f"Dimension 2 ({pct2} variance)")
    plt.axvline(0, color="k", alpha=0.8, linewidth=0.8, zorder=0)
    plt.axhline(0, color="k", alpha=0.8, linewidth=0.8, zorder=0)

    # --- 3D plot ---
    fig3d = plt.figure()
    ax = fig3d.add_subplot(111, projection="3d")

    # Column points (tetrahedron vertices) as diamonds
    col_xyz = {label: (row.iloc[0], row.iloc[1], row.iloc[2])
               for label, row in col_coords.iterrows()}

    for label, (x, y, z) in col_xyz.items():
        ax.scatter(x, y, z, color=colors[label], marker="D", s=60, zorder=5)
        ax.text(x, y, z, f"  {label}", color=colors[label], fontsize=9)

    # Connect every pair of vertices with thin dark grey lines
    for (l1, (x1, y1, z1)), (l2, (x2, y2, z2)) in combinations(col_xyz.items(), 2):
        ax.plot([x1, x2], [y1, y2], [z1, z2], color="#555555", linewidth=0.8, zorder=1)

    # Row points inside the tetrahedron
    for label, row in row_coords.iterrows():
        x, y, z = row.iloc[0], row.iloc[1], row.iloc[2]
        ax.scatter(x, y, z, color=colors[label], s=60, zorder=5)
        ax.text(x, y, z, f"  {label}", color=colors[label], fontsize=9)

    pct3 = summary["% of variance"].iloc[2]
    ax.set_xlabel(f"Dim 1 ({pct1} variance)")
    ax.set_ylabel(f"Dim 2 ({pct2} variance)")
    ax.set_zlabel(f"Dim 3 ({pct3} variance)")

    # Scale the box so each axis length reflects sqrt(eigenvalue),
    # i.e. the actual spread of principal-coordinate points along that axis.
    # This compresses dim 3 visually if it explains very little variance.
    aspect = eigs ** 0.5
    ax.set_box_aspect(aspect / aspect.max())

    plt.tight_layout()
    plt.show()
