import io
import datetime
import requests
import pandas as pd
from typing import List, Tuple

INDEX_CATALOG = [
    ("NIFTY_50", "ind_nifty50list.csv"),
    ("NIFTY_NEXT_50", "ind_niftynext50list.csv"),
    ("NIFTY_100", "ind_nifty100list.csv"),
    ("NIFTY_BANK", "ind_niftybanklist.csv"),
    ("NIFTY_MIDCAP_150", "ind_niftymidcap150list.csv"),
    ("NIFTY_SMALLCAP_250", "ind_niftysmallcap250list.csv"),
    ("NIFTY_500", "ind_nifty500list.csv"),
    ("NIFTY_IT", "ind_niftyitlist.csv"),
    ("NIFTY_AUTO", "ind_niftyautolist.csv"),
    ("NIFTY_FMCG", "ind_niftyfmcglist.csv"),
    ("NIFTY_PHARMA", "ind_niftypharmalist.csv"),
    ("NIFTY_METAL", "ind_niftymetallist.csv"),
    ("NIFTY_ENERGY", "ind_niftyenergylist.csv"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "*/*",
}


class IndexConstituentsFetcher:
    """
    Fetches official constituent listings across NSE Benchmark, Broad Market, 
    and Sectoral indices directly from NSE Indices archives.
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_all_constituents(self) -> pd.DataFrame:
        today_iso = datetime.date.today().isoformat()
        records = []

        for idx_name, filename in INDEX_CATALOG:
            url = f"https://archives.nseindia.com/content/indices/{filename}"
            try:
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 200:
                    df = pd.read_csv(io.StringIO(resp.text))
                    df.columns = [c.strip().replace(" ", "_").upper() for c in df.columns]

                    for _, row in df.iterrows():
                        sym = str(row.get("SYMBOL", "")).strip().upper()
                        isin = str(row.get("ISIN_CODE", "")).strip().upper()
                        comp = str(row.get("COMPANY_NAME", "")).strip()
                        ind = str(row.get("INDUSTRY", "")).strip()
                        ser = str(row.get("SERIES", "EQ")).strip()

                        if sym and sym != "NAN":
                            records.append({
                                "as_of_date": today_iso,
                                "index_name": idx_name,
                                "symbol": sym,
                                "isin": isin,
                                "company_name": comp,
                                "industry": ind,
                                "series": ser,
                                "source": "NSE_INDICES_ARCHIVES"
                            })
            except Exception as e:
                print(f"Warning: Failed to fetch {idx_name} ({filename}): {e}")

        df_out = pd.DataFrame(records)
        # Purge any exchange test/dummy entries that violate SEBI ISIN format
        df_out = df_out[df_out["isin"].str.match(r"^IN[A-Z0-9]{10}$")]
        df_out = df_out.sort_values(by=["index_name", "symbol"]).reset_index(drop=True)
        return df_out
