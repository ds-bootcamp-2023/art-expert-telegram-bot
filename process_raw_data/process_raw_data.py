"""Process raw data and form dataset."""
# import os
import re
import shutil
from math import log10
from pathlib import Path
from statistics import mean

import pandas as pd
from sklearn.model_selection import train_test_split

RAW_DATA_PATH: Path = Path(__file__).parent / "raw_data"
FINAL_DATA_PATH: Path = Path(__file__).parent / "final_data"
CURRENCY_MULTIPLICATORS: dict[str, float] = {"USD": 1.0, "EUR": 1.11, "GBP": 1.25}


def load_orig() -> pd.DataFrame:
    """Load and transform original dataset."""

    df: pd.DataFrame = pd.read_csv(RAW_DATA_PATH / "prices" / "orig.csv", index_col=0)
    df["price"] = df["price"].apply(lambda x: x.split(" ")[0].replace(".", "")).astype(float)
    df["image"] = df.index
    df["image"] = df["image"].apply(lambda x: f"orig/image_{x + 1}.png")

    return df[["price", "artist", "title", "image"]]


def load_artsy() -> pd.DataFrame:
    """Load and transform Artsy dataset."""

    df: pd.DataFrame = pd.read_csv(RAW_DATA_PATH / "prices" / "artsy.csv", index_col=0)
    df = df.rename(columns={"author": "artist"}).drop(columns=["source"])
    df["title"] = df["title"].apply(lambda x: " ".join(x.split(",")[:-1]))
    df["image"] = df.index
    df["image"] = df["image"].apply(lambda x: f"artsy/{x}.jpeg")

    df["currency"] = df["price"].apply(
        lambda x: "USD" if "US$" in x else "EUR" if "€" in x else "GBP" if "£" in x else "OTHER"
    )
    df = df[df["currency"].isin(["USD", "EUR", "GBP"])]
    df["price"] = df["price"].apply(lambda x: [re.sub(r"\D", "", s) for s in x.replace(",", "").split("–")])
    df["price"] = df["price"].apply(lambda x: 10 ** mean([log10(int(y)) for y in x]))
    df["price"] = df.apply(lambda row: row["price"] * CURRENCY_MULTIPLICATORS[row["currency"]], axis=1)

    return df[["price", "artist", "title", "image"]]


def load_bidtoart() -> pd.DataFrame:
    """Load and transform BidToArt dataset."""

    df: pd.DataFrame = pd.read_csv(RAW_DATA_PATH / "prices" / "bidtoart.csv", index_col=0)
    df = df.rename(columns={"author": "artist"})[["artist", "title", "price"]]
    df["image"] = df.index
    df["image"] = df["image"].apply(lambda x: f"bidtoart/{x}.jpg")

    df["currency"] = df["price"].apply(
        lambda x: "OTHER"
        if x == "-"
        else "USD"
        if x.startswith("$")
        else "EUR"
        if x.startswith("€")
        else "GBP"
        if x.startswith("£")
        else "OTHER"
    )
    df = df[df["currency"].isin(["USD", "EUR", "GBP"])]

    df["price"] = df["price"].apply(lambda x: [re.sub(r"\D", "", s) for s in x.split("-")])
    df["price"] = df["price"].apply(lambda x: 10 ** mean([log10(float(y or 1)) for y in x]))
    df["price"] = df.apply(lambda row: row["price"] * CURRENCY_MULTIPLICATORS[row["currency"]], axis=1)

    return df[["price", "artist", "title", "image"]]


def load_menziesartbrands() -> pd.DataFrame:
    """Load and transform Menzie's Art Brands dataset."""

    # for image in os.listdir(RAW_DATA_PATH / "menziesartbrands"):
    #     os.rename(RAW_DATA_PATH / "menziesartbrands" / image, RAW_DATA_PATH / "menziesartbrands" / image.lstrip("0"))

    df: pd.DataFrame = pd.read_csv(RAW_DATA_PATH / "prices" / "menziesartbrands.csv", index_col=0)
    df["image"] = df["image"].apply(lambda x: f"menziesartbrands/{x}")
    return df[["price", "artist", "title", "image"]]


if __name__ == "__main__":
    orig_df: pd.DataFrame = load_orig()
    orig_df["source"] = "orig"
    train, val = train_test_split(orig_df, test_size=0.5, random_state=42)

    artsy_df: pd.DataFrame = load_artsy()
    artsy_df["source"] = "artsy"

    bidtoart_df: pd.DataFrame = load_bidtoart()
    bidtoart_df["source"] = "bidtoart"

    menziesartbrands_df: pd.DataFrame = load_menziesartbrands()
    menziesartbrands_df["source"] = "menziesartbrands"

    train: pd.DataFrame = pd.concat([train, artsy_df, bidtoart_df, menziesartbrands_df])

    train = train.reset_index().drop(columns=["index"])
    val = val.reset_index().drop(columns=["index"])

    for i, row in train.iterrows():
        init_image: Path = RAW_DATA_PATH / row.image
        final_image: Path = FINAL_DATA_PATH / "train" / f"{i}{init_image.suffix}"
        shutil.copy(init_image, final_image)
        train.loc[i, "image"] = final_image.name

    for i, row in val.iterrows():
        init_image: Path = RAW_DATA_PATH / row.image
        final_image: Path = FINAL_DATA_PATH / "val" / f"{i}{init_image.suffix}"
        shutil.copy(init_image, final_image)
        val.loc[i, "image"] = final_image.name

    train.to_csv(FINAL_DATA_PATH / "train.csv", index=False)
    val.to_csv(FINAL_DATA_PATH / "val.csv", index=False)
