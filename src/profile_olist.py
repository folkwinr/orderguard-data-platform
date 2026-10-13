
from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "olist"
REPORT_PATH = PROJECT_ROOT / "docs" / "olist_source_profile.md"

EXPECTED_FILES = {
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
}


def count_missing_references(child_key, parent_key):
    """Count non-null child keys without a matching parent."""
    return int(
        (~child_key.dropna().isin(parent_key.dropna())).sum()
    )


def add_checks(report, title, checks):
    """Add count-based checks to the report and terminal output."""
    report.extend([
        f"## {title}",
        "",
        "| Check | Count |",
        "|---|---:|",
    ])

    print(f"\n{title}")

    for name, count in checks.items():
        count = int(count)
        report.append(f"| {name} | {count:,} |")
        print(f"{name}: {count:,}")

    report.append("")


def main():
    actual_files = {path.name for path in RAW_DIR.glob("*.csv")}

    missing_files = sorted(EXPECTED_FILES - actual_files)
    unexpected_files = sorted(actual_files - EXPECTED_FILES)

    if missing_files or unexpected_files:
        raise ValueError(
            f"Missing CSV files: {missing_files}; "
            f"Unexpected CSV files: {unexpected_files}"
        )

    report = [
        "# Olist Source Data Profile",
        "",
        "Generated from the original Olist CSV files.",
        "Raw source files are not modified.",
        "",
        "Pandas data types are inferred from source values.",
        "They are not final PostgreSQL column definitions.",
        "",
    ]

    # Profile all nine CSV files
    for filename in sorted(EXPECTED_FILES):
        df = pd.read_csv(RAW_DIR / filename, low_memory=False)

        report.extend([
            f"## {filename}",
            "",
            f"- Rows: {len(df):,}",
            f"- Columns: {len(df.columns)}",
            "",
            "| Column | Pandas dtype | Missing | Missing % |",
            "|---|---|---:|---:|",
        ])

        for column in df.columns:
            missing = int(df[column].isna().sum())
            percentage = missing / len(df) * 100 if len(df) else 0

            report.append(
                f"| `{column}` | `{df[column].dtype}` | "
                f"{missing:,} | {percentage:.2f}% |"
            )

        report.append("")

        print(
            f"{filename}: "
            f"{len(df):,} rows, {len(df.columns)} columns"
        )

    # Load columns needed for validation
    orders = pd.read_csv(
        RAW_DIR / "olist_orders_dataset.csv",
        usecols=[
            "order_id",
            "customer_id",
            "order_status",
            "order_approved_at",
            "order_delivered_customer_date",
        ],
    )

    customers = pd.read_csv(
        RAW_DIR / "olist_customers_dataset.csv",
        usecols=["customer_id", "customer_unique_id"],
    )

    items = pd.read_csv(
        RAW_DIR / "olist_order_items_dataset.csv",
        usecols=[
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
        ],
    )

    products = pd.read_csv(
        RAW_DIR / "olist_products_dataset.csv",
        usecols=["product_id", "product_category_name"],
    )

    sellers = pd.read_csv(
        RAW_DIR / "olist_sellers_dataset.csv",
        usecols=["seller_id"],
    )

    payments = pd.read_csv(
        RAW_DIR / "olist_order_payments_dataset.csv",
        usecols=["order_id", "payment_sequential"],
    )

    reviews = pd.read_csv(
        RAW_DIR / "olist_order_reviews_dataset.csv",
        usecols=["order_id", "review_id"],
    )

    categories = pd.read_csv(
        RAW_DIR / "product_category_name_translation.csv",
        usecols=["product_category_name"],
    )

    # Candidate primary key checks
    key_checks = {
        "Duplicate order IDs":
            orders["order_id"].duplicated().sum(),

        "Duplicate customer IDs":
            customers["customer_id"].duplicated().sum(),

        "Duplicate order item keys":
            items.duplicated(
                subset=["order_id", "order_item_id"]
            ).sum(),

        "Duplicate product IDs":
            products["product_id"].duplicated().sum(),

        "Duplicate seller IDs":
            sellers["seller_id"].duplicated().sum(),

        "Duplicate payment keys":
            payments.duplicated(
                subset=["order_id", "payment_sequential"]
            ).sum(),

        "Missing order IDs":
            orders["order_id"].isna().sum(),

        "Missing customer IDs":
            customers["customer_id"].isna().sum(),

        "Missing order item IDs":
            items["order_item_id"].isna().sum(),

        "Missing product IDs":
            products["product_id"].isna().sum(),

        "Missing seller IDs":
            sellers["seller_id"].isna().sum(),
    }

    add_checks(report, "Key Checks", key_checks)

    # Referential integrity checks
    relationship_checks = {
        "Orders without a matching customer":
            count_missing_references(
                orders["customer_id"],
                customers["customer_id"],
            ),

        "Customers without a matching order":
            count_missing_references(
                customers["customer_id"],
                orders["customer_id"],
            ),

        "Order items without a matching order":
            count_missing_references(
                items["order_id"],
                orders["order_id"],
            ),

        "Order items without a matching product":
            count_missing_references(
                items["product_id"],
                products["product_id"],
            ),

        "Order items without a matching seller":
            count_missing_references(
                items["seller_id"],
                sellers["seller_id"],
            ),

        "Payments without a matching order":
            count_missing_references(
                payments["order_id"],
                orders["order_id"],
            ),

        "Reviews without a matching order":
            count_missing_references(
                reviews["order_id"],
                orders["order_id"],
            ),

        "Products with unmatched non-null categories":
            count_missing_references(
                products["product_category_name"],
                categories["product_category_name"],
            ),
    }

    add_checks(
        report,
        "Referential Integrity Checks",
        relationship_checks,
    )

    # Identify orders without related records
    orders_without_items = orders.loc[
        ~orders["order_id"].isin(items["order_id"])
    ]

    orders_without_payments = orders.loc[
        ~orders["order_id"].isin(payments["order_id"])
    ]

    orders_without_reviews = orders.loc[
        ~orders["order_id"].isin(reviews["order_id"])
    ]

    descriptive_checks = {
        "Orders without order items":
            len(orders_without_items),

        "Orders without payments":
            len(orders_without_payments),

        "Orders without reviews":
            len(orders_without_reviews),

        "Unique customers":
            customers["customer_unique_id"].nunique(),

        "Customers with multiple customer records":
            (
                customers["customer_unique_id"]
                .value_counts() > 1
            ).sum(),

        "Delivered orders without a delivery date":
            (
                (orders["order_status"] == "delivered")
                & orders["order_delivered_customer_date"].isna()
            ).sum(),
    }

    add_checks(
        report,
        "Descriptive Findings",
        descriptive_checks,
    )

    # Show orders without items by order status
    report.extend([
        "## Orders Without Items by Status",
        "",
        "| Order status | Orders |",
        "|---|---:|",
    ])

    for status, count in (
        orders_without_items["order_status"]
        .value_counts()
        .items()
    ):
        report.append(f"| `{status}` | {count:,} |")

    report.append("")

    # Show individual orders without payment records
    report.extend([
        "## Orders Without Payment Records",
        "",
        "| Order ID | Status | Approved At | Delivered At |",
        "|---|---|---|---|",
    ])

    for _, row in orders_without_payments.iterrows():
        approved = (
            str(row["order_approved_at"])
            if pd.notna(row["order_approved_at"])
            else "NULL"
        )

        delivered = (
            str(row["order_delivered_customer_date"])
            if pd.notna(row["order_delivered_customer_date"])
            else "NULL"
        )

        report.append(
            f"| `{row['order_id']}` | `{row['order_status']}` | "
            f"{approved} | {delivered} |"
        )

    report.append("")

    # Find product categories missing from the translation table
    unmatched_categories = products.loc[
        products["product_category_name"].notna()
        & ~products["product_category_name"].isin(
            categories["product_category_name"]
        ),
        "product_category_name",
    ]

    report.extend([
        "## Unmatched Product Categories",
        "",
        "| Original category | Product records |",
        "|---|---:|",
    ])

    for category, count in unmatched_categories.value_counts().items():
        report.append(f"| `{category}` | {count:,} |")

    report.append("")

    # Summarize one-to-many relationship cardinality
    report.extend([
        "## Relationship Cardinality",
        "",
        "| Child table | Distinct orders | Orders with multiple rows | Maximum rows per order |",
        "|---|---:|---:|---:|",
    ])

    for name, frame in [
        ("Order items", items),
        ("Payments", payments),
        ("Reviews", reviews),
    ]:
        counts = frame.groupby("order_id").size()

        report.append(
            f"| {name} | {frame['order_id'].nunique():,} | "
            f"{int((counts > 1).sum()):,} | "
            f"{int(counts.max()) if len(counts) else 0:,} |"
        )

    report.extend([
        "",
        "## Interpretation Notes",
        "",
        "- These are source profiling results, not final quality verdicts.",
        "- Orders without items may be explained by their status.",
        "- A delivered order without a payment record requires investigation.",
        "- Missing category translations require reference data handling.",
        "- Missing reviews do not automatically indicate invalid orders.",
        "- Referential checks exclude null child keys; "
        "missingness is reported separately.",
        "- Geolocation ZIP prefixes are not unique primary keys.",
        "- ZIP code prefixes should be represented as text "
        "in the target schema.",
        "- Original CSV files are not modified.",
        "- No PostgreSQL ingestion or quarantine actions "
        "are performed by this script.",
        "",
    ])

    # Save the English-language Markdown report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    REPORT_PATH.write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    print(f"\nReport saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
