import requests
from bs4 import BeautifulSoup
import re

URLS = [
    "https://az24.vn/xsmb-sxmb-xo-so-mien-bac.html",
    "https://mketqua.net/so-ket-qua-truyen-thong/300",
    "https://mketqua.net/tan-suat-loto"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extract(text):
    return re.findall(r"\b\d{2}\b", text)

def crawl():
    data = []

    for url in URLS:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            nums = extract(soup.get_text(" "))
            data.extend(nums)

        except:
            continue

    return data
