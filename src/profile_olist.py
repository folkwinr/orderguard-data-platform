
from pathlib import Path

import pandas as pd


# Directory containing the original Olist CSV files
RAW_DIR = Path("data/raw/olist")

# Output path for the generated data profiling report
REPORT_PATH = Path("docs/olist_source_profile.md")


def main():
    csv_files = sorted(RAW_DIR.glob("*.csv"))

    # Verify that all 9 expected source files are present
    if len(csv_files) != 9:
        raise ValueError(
            f"Expected 9 CSV files, but found {len(csv_files)}."
        )

    report = [
        "# Olist Source Data Profile",
        "",
        "This report is generated from the original Olist CSV files.",
        "Raw source files are not modified.",
        "",
    ]

    # Profile each source CSV file
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, low_memory=False)

        report.extend([
            f"## {csv_file.name}",
            "",
            f"- Rows: {len(df):,}",
            f"- Columns: {len(df.columns)}",
            "",
            "| Column | Pandas dtype | Missing | Missing % |",
            "|---|---|---:|---:|",
        ])

        for column in df.columns:
            missing = int(df[column].isna().sum())
            percentage = (missing / len(df) * 100) if len(df) else 0

            report.append(
                f"| `{column}` | `{df[column].dtype}` | "
                f"{missing:,} | {percentage:.2f}% |"
            )

        report.append("")

        print(
            f"{csv_file.name}: "
            f"{len(df):,} rows, {len(df.columns)} columns"
        )

    # Load the columns required for key and relationship checks
    orders = pd.read_csv(
        RAW_DIR / "olist_orders_dataset.csv",
        usecols=["order_id", "customer_id"]
    )

    customers = pd.read_csv(
        RAW_DIR / "olist_customers_dataset.csv",
        usecols=["customer_id"]
    )

    items = pd.read_csv(
        RAW_DIR / "olist_order_items_dataset.csv",
        usecols=["order_id", "order_item_id"]
    )

    # Check key uniqueness and referential integrity
    checks = {
        "Duplicate order IDs": (
            orders["order_id"].duplicated().sum()
        ),
        "Duplicate customer IDs": (
            customers["customer_id"].duplicated().sum()
        ),
        "Duplicate order item keys": (
            items.duplicated(
                subset=["order_id", "order_item_id"]
            ).sum()
        ),
        "Orders without a matching customer": (
            ~orders["customer_id"].isin(customers["customer_id"])
        ).sum(),
        "Order items without a matching order": (
            ~items["order_id"].isin(orders["order_id"])
        ).sum(),
        "Orders without order items": (
            ~orders["order_id"].isin(items["order_id"])
        ).sum(),
    }

    # Add validation results to the report
    report.extend([
        "## Key and Relationship Checks",
        "",
        "| Check | Count |",
        "|---|---:|",
    ])

    for check, count in checks.items():
        report.append(f"| {check} | {count:,} |")
        print(f"{check}: {count:,}")

    report.append("")

    # Create the report directory if it does not exist
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save the profiling results as a Markdown document
    REPORT_PATH.write_text(
        "\n".join(report) + "\n",
        encoding="utf-8"
    )

    print(f"\nReport saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
