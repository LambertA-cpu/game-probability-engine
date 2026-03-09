import requests
from bs4 import BeautifulSoup
import pandas as pd


URL = "https://mylottokenya.co.ke/jackpot-results"


def fetch_lotto_results():

    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table")

    rows = table.find_all("tr")

    data = []

    for row in rows[1:]:

        cols = row.find_all("td")

        if len(cols) >= 2:

            date = cols[0].text.strip()

            nums = cols[1].text.strip()

            nums = nums.replace(" ", "")
            nums = nums.split(",")

            nums = [int(n) for n in nums]

            data.append({
                "date": date,
                "numbers": nums
            })

    return pd.DataFrame(data)