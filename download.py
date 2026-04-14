from os import remove
import re

import numpy as np
import pandas as pd
import pyreadr
import requests


def taste():
    url = "https://raw.githubusercontent.com/cran/soc.ca/master/data/taste.rda"
    with open("taste.rda", "wb") as f:
        f.write(requests.get(url).content)

    result = pyreadr.read_r("taste.rda")
    remove("taste.rda")
    df = result["taste"]
    df.to_csv("taste/data.csv", index=False)
    print("Downloaded taste dataset to taste/data.csv")


def hair_eye_color():
    url = "https://raw.githubusercontent.com/wch/r-source/trunk/src/library/datasets/data/HairEyeColor.R"
    r_code = requests.get(url).text

    # Extract the data values from the c(...) part of the array() call
    match = re.search(r'array\(c\((.+?)\)\s*,\s*dim', r_code, re.DOTALL)
    nums = list(map(int, re.findall(r'\d+', match.group(1))))

    hair = ["Black", "Brown", "Red", "Blond"]
    eye = ["Brown", "Blue", "Hazel", "Green"]

    # R stores arrays in column-major order: dim = c(4, 4, 2) means Hair varies fastest
    # The source file has duplicate values; take only the first 4*4*2 = 32
    arr = np.array(nums[:32]).reshape((4, 4, 2), order='F')  # arr[hair, eye, sex]

    for sex_idx, sex in enumerate(["Male", "Female"]):
        df = pd.DataFrame(arr[:, :, sex_idx], index=hair, columns=eye)
        df.index.name = "Hair\\Eye"
        df.to_csv(f"color/data_{sex.lower()}.csv")

    combined = pd.DataFrame(arr.sum(axis=2), index=hair, columns=eye)
    combined.index.name = "Hair\\Eye"
    combined.to_csv("color/data.csv")
    print("Downloaded HairEyeColor dataset to color/data.csv (combined) and color/data_male.csv, color/data_female.csv")
    

if __name__ == "__main__":
    hair_eye_color()
    taste()

