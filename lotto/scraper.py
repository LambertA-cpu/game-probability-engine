import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://mylottokenya.co.ke/jackpot-results"

def scrape_lotto_results():

    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")

    data = []

    for row in rows[1:]:
        cols = row.find_all("td")

        if len(cols) >= 2:

            date = cols[0].text.strip()

            numbers = cols[1].text.strip()
            numbers = numbers.replace(" ", "")
            numbers = numbers.split(",")

            numbers = [int(n) for n in numbers]

            data.append({
                "date": date,
                "numbers": numbers
            })

    return pd.DataFrame(data)