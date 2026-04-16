import pandas as pd

TAB_PATH = "./UKDA-5832-tab/tab/ccse_main_sample_file.tab"

MUSIC_TASTE     = ['Rock', 'MJazz', 'World', 'Classica', 'CandW', 'Electron', 'HeavyM', 'Urban']
MUSIC_KNOWLEDGE = ['Wonderw', 'Stan', 'FourSeas', 'EinStein', 'Symph5', 'KindBlue', 'Oops', 'Chicago']
VISUAL_ART      = ['ArtM', 'ArtL', 'VanGogh', 'Picasso', 'Kahlo', 'Turner', 'Emin', 'Warhol', 'Lowry']
FILM            = ['FilmM', 'FilmS', 'FilmL', 'Spielb', 'Hitchc', 'Almodov', 'Bergman', 'Campion', 'Rathnam']
EATING          = ['EatM', 'EatS', 'EatL']
PARTICIPATION   = ['Cinema', 'Museum', 'Pub', 'Rockconc', 'Opera', 'Bingo', 'Orchconc',
                   'StatelyH', 'Musical', 'Theatre', 'ArtGall', 'NightC', 'EatOut']
TV              = ['TypProgM', 'TypProgS', 'TypProgL', 'TVHrsWkD']
SPORT           = ['SportM', 'SportS', 'SportL', 'AnySport']
READING         = ['WhoDun', 'SciFi', 'Romance', 'Biog', 'Modlit', 'Relig', 'Selfhelp', 'ManyBook']
SOCDEM          = ['RAge', 'RSex', 'RAgeCat', 'WtFactor']

ACTIVE_VARS = (MUSIC_TASTE + MUSIC_KNOWLEDGE + VISUAL_ART + FILM + EATING +
               PARTICIPATION + TV + SPORT + READING)
# Note: TVProg1, TVProg2, TVProg3 (specific TV show preferences) are excluded:
# those 24-category variables inflate TV taste and are not used by Le Roux.
ALL_VARS = ACTIVE_VARS + SOCDEM

# Domain assignments: domain → participation variables, taste variables
# The 10 standard participation items are distributed across domains by venue type.
# TVHrsWkD, ManyBook, AnySport are also participation measures.
DOMAIN_VARS = {
    'TV': {
        'participation': ['TVHrsWkD'],
        'taste':         ['TypProgM', 'TypProgS', 'TypProgL'],
    },
    'Films': {
        'participation': ['Cinema'],
        'taste':         ['FilmM', 'FilmS', 'FilmL', 'Spielb', 'Hitchc', 'Almodov',
                          'Bergman', 'Campion', 'Rathnam'],
    },
    'Reading': {
        'participation': ['ManyBook'],
        'taste':         ['WhoDun', 'SciFi', 'Romance', 'Biog', 'Modlit', 'Relig', 'Selfhelp'],
    },
    'Music': {
        'participation': ['Rockconc', 'Opera', 'Orchconc', 'Musical', 'NightC'],
        'taste':         MUSIC_TASTE + MUSIC_KNOWLEDGE,
    },
    'Visual art': {
        'participation': ['Museum', 'ArtGall', 'StatelyH', 'Theatre'],
        'taste':         VISUAL_ART,
    },
    'Eating out': {
        'participation': ['Pub', 'EatOut', 'Bingo'],
        'taste':         EATING,
    },
    'Sport': {
        'participation': ['AnySport'],
        'taste':         ['SportM', 'SportS', 'SportL'],
    },
}

# Le Roux Table 1 for comparison
LEROUX = pd.DataFrame({
    'TV':         {'Participation': 3.2,  'Taste': 11.2},
    'Films':      {'Participation': 1.6,  'Taste': 12.1},
    'Reading':    {'Participation': 4.0,  'Taste': 11.2},
    'Music':      {'Participation': 7.9,  'Taste': 11.2},
    'Visual art': {'Participation': 6.3,  'Taste':  9.7},
    'Eating out': {'Participation': 3.2,  'Taste':  6.4},
    'Sport':      {'Participation': 4.0,  'Taste':  8.1},
})


def active_cat_count(series, weights, threshold=0.04):
    """Number of categories with weighted relative frequency >= threshold.

    Frequency is computed over the full sample (including non-respondents),
    matching Le Roux's 4% cut: a modality must represent >=4% of all 1564
    respondents, not just those who answered the question.
    """
    mask = series.notna()
    s, w = series[mask], weights[mask]
    total_w = weights.sum()   # denominator = full sample weight
    wfreq = s.groupby(s).apply(lambda g: w.loc[g.index].sum()) / total_w
    return int((wfreq >= threshold).sum())


if __name__ == "__main__":
    tab = pd.read_csv(TAB_PATH, sep="\t")
    tab.columns = tab.columns.str.lower()

    all_lower = [v.lower() for v in ALL_VARS]
    available = [v for v in all_lower if v in tab.columns]
    missing   = [v for v in all_lower if v not in tab.columns]
    if missing:
        print("Variables not found:", missing)

    df = tab[available].copy()
    lower_to_orig = {v.lower(): v for v in ALL_VARS}
    df.columns = [lower_to_orig.get(c, c) for c in df.columns]

    # Recode don't-know / refusal / skip as NaN
    for col in df.columns:
        if col == 'WtFactor':
            continue
        if df[col].max() <= 9:
            df[col] = df[col].replace({8: pd.NA, 9: pd.NA, -1: pd.NA})
        else:
            df[col] = df[col].replace({97: pd.NA, 98: pd.NA, 99: pd.NA, -1: pd.NA})

    # Recode 1–7 Likert taste scales to three levels matching Le Roux's +/=/− modalities
    LIKERT_7 = MUSIC_TASTE + ['WhoDun', 'SciFi', 'Romance', 'Biog', 'Modlit', 'Relig', 'Selfhelp']
    for col in LIKERT_7:
        if col in df.columns:
            df[col] = df[col].map({1: '-', 2: '-', 3: '-', 4: '=', 5: '+', 6: '+', 7: '+'})

    # Bin continuous/count variables into categorical levels
    df['TVHrsWkD'] = pd.cut(
        pd.to_numeric(df['TVHrsWkD'], errors='coerce'),
        bins=[-1, 1, 3, 5, float('inf')],
        labels=['0-1h', '2-3h', '4-5h', '>5h'],
    )
    df['ManyBook'] = pd.cut(
        df['ManyBook'].astype(float),
        bins=[-1, 0, 6, 24, float('inf')],
        labels=['noBk', '1-6', '7-24', '>24'],
    )

    weights = df['WtFactor']

    # Count active modalities (K_q) and variables (Q) per domain × split cell
    records = {}
    for domain, splits in DOMAIN_VARS.items():
        for split, var_list in splits.items():
            present = [v for v in var_list if v in df.columns]
            k_minus_q = sum(active_cat_count(df[v], weights) - 1 for v in present)
            records[(domain, split)] = k_minus_q

    total_k_minus_q = sum(records.values())

    # Convert to % of total inertia
    pct = {key: round(val / total_k_minus_q * 100, 1) for key, val in records.items()}

    result = pd.DataFrame(pct, index=[0]).T
    result.index = pd.MultiIndex.from_tuples(result.index, names=['Domain', 'Split'])
    result = result[0].unstack('Split')[['participation', 'taste']]
    result.columns = ['Participation', 'Taste']
    result['Total'] = (result['Participation'] + result['Taste']).round(1)

    # Add totals row
    result.loc['Total'] = result.sum().round(1)

    print("Our calculation:")
    print(result.to_string())

    print("\nLe Roux Table 1:")
    lr = LEROUX.T
    lr['Total'] = lr.sum(axis=1).round(1)
    lr.loc['Total'] = lr.sum().round(1)
    print(lr.to_string())

    print(f"\nTotal K−Q: {total_k_minus_q}  (Le Roux use 166 active modalities − 41 variables = 125? "
          f"or 198−41=157?)")
