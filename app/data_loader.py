import pandas as pd

def load_lottery_data(path: str):
    df = pd.read_csv(path)

    df["numbers"] = df["numbers"].apply(
        lambda x: [int(n.strip()) for n in x.split(",")]
    )

    return df
