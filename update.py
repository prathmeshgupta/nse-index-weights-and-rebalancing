"""
Automated Weekly Dataset Updater for nse-index-weights-and-rebalancing
Can be executed locally or via GitHub Actions.
Zero credentials required.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import pandas as pd
from nse_index_weights.fetcher import IndexConstituentsFetcher

OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = OUTPUT_DIR / "index_constituents.csv"
PARQUET_FILE = OUTPUT_DIR / "index_constituents.parquet"


def update():
    print("[1/3] Fetching latest index constituent memberships from official NSE archives...")
    fetcher = IndexConstituentsFetcher()
    new_df = fetcher.fetch_all_constituents()
    print(f"      Retrieved {len(new_df)} index constituent records across {new_df['index_name'].nunique()} indices.")

    print("[2/3] Merging and saving updated index constituent datasets...")
    if CSV_FILE.exists():
        existing_df = pd.read_csv(CSV_FILE)
        combined = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined = new_df.copy()

    combined = combined[combined["isin"].str.match(r"^IN[A-Z0-9]{10}$")]
    combined = combined.drop_duplicates(subset=["as_of_date", "index_name", "symbol"], keep="last")
    combined = combined.sort_values(by=["as_of_date", "index_name", "symbol"], ascending=[False, True, True])

    combined.to_csv(CSV_FILE, index=False)
    combined.to_parquet(PARQUET_FILE, index=False)
    print(f"      Saved {len(combined)} records to {CSV_FILE.name} and {PARQUET_FILE.name}.")

    print("[3/3] Running automated quality audit...")
    from evaluate_quality import audit_quality
    audit_quality()
    print("Update complete successfully.")


if __name__ == "__main__":
    update()
