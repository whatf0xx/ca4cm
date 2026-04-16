# ca4cm — (Multiple) Correspondence Analysis

Code and slides for a 20-minute tutorial on correspondence analysis (CA) and multiple correspondence analysis (MCA), prepared for the [Complexity Science Hub](https://csh.ac.at) lab group.

## Installation

```bash
git clone https://github.com/whatf0xx/ca4cm.git
cd ca4cm
python -m venv .venv
source .venv/bin/activate
pip install matplotlib numpy pandas prince
```

## Running the examples

All scripts are run from the **repository root**.

### Example 1 — Hair and eye colour (CA)

```bash
python color/ca.py
```

Reads `color/data.csv` and writes `2d-color.pdf` and `3d_proj.pdf`.

### Example 2 — Vienna national election results 2024 (CA)

```bash
python wahlkreis/ca.py
```

Reads `wahlkreis/NR241.csv` and writes `wahlkreis_asymmetric.pdf` and `symmetric_wahlkreis.pdf`.

### Example 3 — Class and cultural division in the UK (MCA)

```bash
python taste/mca.py
```

Reads `taste/data.csv` (derived from the `taste` dataset in the [`soc.ca`](https://github.com/cran/soc.ca) R package) and writes `active_taste_cols.pdf` and `supp_taste_cols.pdf`.

## Data

All data files needed to run the three main examples are committed to the repository. `download.py` was used to fetch and process the original source files and does not need to be re-run.

## Building the slides

The slides are written in LaTeX Beamer. With a TeX Live installation and `biber` available:

```bash
make
```

## References

- **prince** — Halford, M. *Prince: Principal component analysis in Python.* [github.com/MaxHalford/prince](https://github.com/MaxHalford/prince)

- **Greenacre, M.** (2017). *Correspondence Analysis in Practice, Third Edition.* Chapman & Hall / CRC Press.

- **Le Roux, B., Rouanet, H., Savage, M., & Warde, A.** (2008). Class and Cultural Division in the UK. *Sociology*, 42(6), 1049–1071.

(A few more are given at the end of the slide deck)
