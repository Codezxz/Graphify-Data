import argparse
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt

# ────────────────────────────────────────────────────────────────────────────────
# 1. DATA LOADING
# ────────────────────────────────────────────────────────────────────────────────
def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    if not path.exists():
        sys.exit(f"File not found: {path}")
    df = pd.read_csv(path)
    print(f"Loaded {len(df):,} rows from {path.name}")
    return df


def choose_file_gui() -> Path:
    """Open a native file-picker if no --file argument passed."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not file_path:
        sys.exit(" No file selected. Exiting.")
    return Path(file_path)

# ────────────────────────────────────────────────────────────────────────────────
# 2. EXPLORATION HELPERS
# ────────────────────────────────────────────────────────────────────────────────
def basic_eda(df: pd.DataFrame) -> None:
    """Print basic DataFrame insights."""
    print("\nColumns:", list(df.columns))
    print("\nMissing Values:\n", df.isna().sum())
    print("\nSummary Stats:\n", df.describe(include="all"))


# ────────────────────────────────────────────────────────────────────────────────
# 3. ANALYSIS EXAMPLES
# ────────────────────────────────────────────────────────────────────────────────
def sales_by_product(df: pd.DataFrame) -> None:
    """Aggregate and plot total sales per product (expects 'Product', 'Sales')."""
    if {"Product", "Sales"}.issubset(df.columns):
        agg = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)
        print("\nSales by Product:\n", agg)

        agg.plot(kind="bar", title="Sales by Product", ylabel="Total Sales", figsize=(10, 5))
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()


def monthly_sales_trend(df: pd.DataFrame) -> None:
    """Plot monthly sales trend (expects 'Date', 'Sales')."""
    if {"Date", "Sales"}.issubset(df.columns):
        df = df.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.to_period("M")
        trend = df.groupby("Month")["Sales"].sum()

        trend.plot(marker="o", title="Monthly Sales Trend", ylabel="Total Sales", figsize=(10, 5))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


# ────────────────────────────────────────────────────────────────────────────────
# 4. MAIN ENTRYPOINT
# ────────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Sales CSV analysis with Pandas.")
    parser.add_argument("--file", "-f", type=Path, help="Path to a CSV file")
    args = parser.parse_args()

    csv_path = args.file or choose_file_gui()
    df = load_csv(csv_path)

    basic_eda(df)
    sales_by_product(df)
    monthly_sales_trend(df)

    out_path = csv_path.with_stem(csv_path.stem + "_cleaned")
    df.to_csv(out_path, index=False)
    print(f"\nCleaned data written to {out_path}")

if __name__ == "__main__":
    main()
