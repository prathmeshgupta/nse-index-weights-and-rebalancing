# NSE Benchmark & Sectoral Index Constituents Dataset

[![Weekly Update](https://github.com/prathmeshgupta/nse-index-weights-and-rebalancing/actions/workflows/update.yml/badge.svg)](https://github.com/prathmeshgupta/nse-index-weights-and-rebalancing/actions/workflows/update.yml)
[![Format: Parquet](https://img.shields.io/badge/Format-Apache%20Parquet-blue.svg)](output/index_constituents.parquet)
[![Format: CSV](https://img.shields.io/badge/Format-CSV-green.svg)](output/index_constituents.csv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An institutional quantitative dataset tracking historical and active constituent memberships across all major **NSE Benchmark, Broad Market, and Thematic/Sectoral Indices** directly from official NSE Indices archives.

Indispensable for index arbitrage, tracking pre-inclusion drift, anti-survivorship universe modeling, and institutional passive flow forecasting.

---

## Benchmark Indices Tracked

* **Broad Market Indices:** `NIFTY_50`, `NIFTY_NEXT_50`, `NIFTY_100`, `NIFTY_MIDCAP_150`, `NIFTY_SMALLCAP_250`, `NIFTY_500`
* **Sectoral Indices:** `NIFTY_BANK`, `NIFTY_IT`, `NIFTY_AUTO`, `NIFTY_FMCG`, `NIFTY_PHARMA`, `NIFTY_METAL`, `NIFTY_ENERGY`

---

## Dataset Schema (`output/index_constituents.parquet` / `.csv`)

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `as_of_date` | `string` | ISO-8601 Snapshot Date (`YYYY-MM-DD`) |
| `index_name` | `string` | Benchmark Index Name (e.g. `NIFTY_50`, `NIFTY_MIDCAP_150`) |
| `symbol` | `string` | NSE Trading Symbol (e.g. `RELIANCE`, `TCS`, `INFY`) |
| `isin` | `string` | Regulatory ISIN Identifier (`^IN[A-Z0-9]{10}$`) |
| `company_name` | `string` | Official Corporate Entity Name |
| `industry` | `string` | Official NSE Industry Classification |
| `series` | `string` | Trading series (`EQ`, `BE`, etc.) |
| `source` | `string` | Data source identifier (`NSE_INDICES_ARCHIVES`) |

---

## Quick Start (Python / Polars / DuckDB)

```python
import polars as pl

# Read directly from GitHub Raw Parquet
url = "https://github.com/prathmeshgupta/nse-index-weights-and-rebalancing/raw/main/output/index_constituents.parquet"
df = pl.read_parquet(url)

# Find all stocks currently in Nifty 50
nifty50 = df.filter(pl.col("index_name") == "NIFTY_50")
print(nifty50.select(["symbol", "company_name", "industry"]))
```
