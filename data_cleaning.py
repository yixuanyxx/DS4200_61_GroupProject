"""
DS4200 Group Project — Step 1: Data Cleaning
Author: Yuansi (Person 1)

Output:
    superstore_clean.csv   ← cleaned dataset used by all viz scripts

Usage:
    python data_cleaning.py
"""

import pandas as pd

# ── CONFIG ─────────────────────────────────────────────────────────────────────
INPUT_FILE  = "Sample - Superstore.csv"
OUTPUT_FILE = "superstore_clean.csv"


# ── LOAD ───────────────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT_FILE, encoding="latin-1")
print(f"Loaded: {len(df):,} rows × {len(df.columns)} columns")


# ── CLEAN ──────────────────────────────────────────────────────────────────────

# 1. Parse dates
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  format="%m/%d/%Y")

# 2. Remove duplicates
before = len(df)
df = df.drop_duplicates()
print(f"Duplicates removed: {before - len(df)}")

# 3. Engineer helper columns
df["Year"]       = df["Order Date"].dt.year
df["Month"]      = df["Order Date"].dt.to_period("M").dt.to_timestamp()
df["YearMonth"]  = df["Order Date"].dt.to_period("M").astype(str)

# 4. Sanity check
assert df.isnull().sum().sum() == 0, "Unexpected nulls found!"
print(f"Null check passed ✓")
print(f"Date range: {df['Order Date'].min().date()} → {df['Order Date'].max().date()}")
print(f"Years: {sorted(df['Year'].unique())}")
print("\nKey stats:")
print(df[["Sales", "Discount", "Profit"]].describe().round(2))


# ── SAVE ───────────────────────────────────────────────────────────────────────
df.to_csv(OUTPUT_FILE, index=False)
print(f"\n✅ Saved cleaned data → {OUTPUT_FILE}")