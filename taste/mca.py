import matplotlib.pyplot as plt
import pandas as pd
from prince import MCA


TAB_PATH = "./UKDA-5832-tab/tab/ccse_main_sample_file.tab"

MUSIC_TASTE     = ['Rock', 'MJazz', 'World', 'Classica', 'CandW', 'Electron', 'HeavyM', 'Urban']
MUSIC_KNOWLEDGE = ['Wonderw', 'Stan', 'FourSeas', 'EinStein', 'Symph5', 'KindBlue', 'Oops', 'Chicago']
VISUAL_ART      = ['ArtM', 'ArtL', 'VanGogh', 'Picasso', 'Kahlo', 'Turner', 'Emin', 'Warhol', 'Lowry']
FILM            = ['FilmM', 'FilmS', 'FilmL', 'Spielb', 'Hitchc', 'Almodov', 'Bergman', 'Campion', 'Rathnam']
EATING          = ['EatM', 'EatS', 'EatL']
PARTICIPATION   = ['Cinema', 'Museum', 'Pub', 'Rockconc', 'Opera', 'Orchconc',
                   'StatelyH', 'Musical', 'Theatre', 'ArtGall']
TV              = ['TypProgM', 'TypProgS', 'TypProgL', 'TVProg1', 'TVProg2', 'TVProg3', 'TVHrsWkD']
SPORT           = ['SportM', 'SportS', 'SportL', 'AnySport']
READING         = ['WhoDun', 'SciFi', 'Romance', 'Biog', 'Modlit', 'Relig', 'Selfhelp', 'ManyBook']
SOCDEM          = ['RAge', 'RSex', 'RAgeCat', 'WtFactor']

ACTIVE_VARS = (MUSIC_TASTE + MUSIC_KNOWLEDGE + VISUAL_ART + FILM + EATING +
               PARTICIPATION + TV + SPORT + READING)
ALL_VARS    = ACTIVE_VARS + SOCDEM


if __name__ == "__main__":
    tab = pd.read_csv(TAB_PATH, sep="\t")

    tab.columns = tab.columns.str.lower()
    all_lower   = [v.lower() for v in ALL_VARS]

    available = [v for v in all_lower if v in tab.columns]
    missing   = [v for v in all_lower if v not in tab.columns]
    if missing:
        print("Not found (check case):", missing)

    df = tab[available].copy()
    # Restore original capitalisation for readability
    lower_to_orig = {v.lower(): v for v in ALL_VARS}
    df.columns = [lower_to_orig.get(c, c) for c in df.columns]

    # Recode don't-know / refusal / skip as NaN
    for col in df.columns:
        if df[col].max() <= 9:
            df[col] = df[col].replace({8: pd.NA, 9: pd.NA, -1: pd.NA})
        else:
            df[col] = df[col].replace({98: pd.NA, 99: pd.NA, -1: pd.NA})

    print(df.shape)
    print(df.head())
