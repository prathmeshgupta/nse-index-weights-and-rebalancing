import re
import pandas as pd
from pathlib import Path

ISO_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ISIN_REGEX = re.compile(r"^IN[A-Z0-9]{10}$")


def audit_quality():
    print("=" * 65)
    print(" NSE INDEX CONSTITUENTS & REBALANCING - DATA QUALITY AUDIT")
    print("=" * 65)

    root = Path(__file__).parent
    pq_path = root / "output" / "index_constituents.parquet"
    csv_path = root / "output" / "index_constituents.csv"

    assert pq_path.exists(), "index_constituents.parquet missing"
    assert csv_path.exists(), "index_constituents.csv missing"

    df_pq = pd.read_parquet(pq_path)
    df_csv = pd.read_csv(csv_path)

    # 1. Parity Check
    assert len(df_pq) == len(df_csv), f"Parity mismatch: Parquet ({len(df_pq)}) != CSV ({len(df_csv)})"
    print(f"Total Index Constituents: {len(df_pq)} [PASS - 100% Parity]")

    # 2. Identifiers & Dates
    null_sym = df_pq["symbol"].isnull().sum()
    null_isin = df_pq["isin"].isnull().sum()
    null_idx = df_pq["index_name"].isnull().sum()
    assert null_sym == 0, f"Found {null_sym} null symbols"
    assert null_isin == 0, f"Found {null_isin} null ISINs"
    assert null_idx == 0, f"Found {null_idx} null index names"
    print("Null Symbols, ISINs & Index Names: 0 [PASS]")

    # 3. ISO-8601 & ISIN Regex
    invalid_dt = df_pq["as_of_date"][~df_pq["as_of_date"].str.match(ISO_REGEX)]
    assert len(invalid_dt) == 0, f"Found {len(invalid_dt)} non-ISO dates"
    print("ISO-8601 Format (as_of_date): 100% PASS")

    invalid_isin = df_pq["isin"][~df_pq["isin"].str.match(ISIN_REGEX)]
    assert len(invalid_isin) == 0, f"Found {len(invalid_isin)} invalid ISINs: {invalid_isin.tolist()[:3]}"
    print("Regulatory ISIN Integrity (^IN[A-Z0-9]{10}$): 100% PASS")

    # 4. Benchmark Index Quotas
    idx_counts = df_pq["index_name"].value_counts()
    print("\nConstituents per Benchmark Index:")
    for idx, cnt in idx_counts.items():
        print(f"  • {idx:<22}: {cnt:>4} securities")

    assert idx_counts.get("NIFTY_50", 0) == 50, "NIFTY_50 count mismatch"
    assert idx_counts.get("NIFTY_NEXT_50", 0) == 50, "NIFTY_NEXT_50 count mismatch"
    assert idx_counts.get("NIFTY_100", 0) == 100, "NIFTY_100 count mismatch"
    assert idx_counts.get("NIFTY_MIDCAP_150", 0) == 150, "NIFTY_MIDCAP_150 count mismatch"
    assert idx_counts.get("NIFTY_SMALLCAP_250", 0) == 250, "NIFTY_SMALLCAP_250 count mismatch"
    assert idx_counts.get("NIFTY_500", 0) == 500, "NIFTY_500 count mismatch"

    print("=" * 65)
    print("ALL AUDIT CHECKS PASSED.")
    print("=" * 65)


if __name__ == "__main__":
    audit_quality()
