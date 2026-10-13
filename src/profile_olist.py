
"""OrderGuard | Stage 1: General Data Profiling.

QUESTION:
What files, tables, and columns do we have?

WHY:
We need a clear source overview before deeper research.

METHOD:
Read the nine Olist CSV files and calculate basic metrics.

OUTPUT:
docs/olist_source_profile.md

This script only describes the source data.
It does not check business rules, keys, or relationships.
It never changes a source CSV or connects to PostgreSQL.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

# Find the project root from this Python file.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Folder with the original Olist CSV files.
SOURCE_DIR = PROJECT_ROOT / "data" / "raw" / "olist"

# The English report is saved here.
REPORT_FILE = PROJECT_ROOT / "docs" / "olist_source_profile.md"


# --------------------------------------------------
# 2. EXPECTED SOURCE SCHEMA
# --------------------------------------------------

# We expect nine CSV files and 52 columns in total.
# Column names and their order must match the source.
#
# This is a basic schema check, not canonical mapping.

EXPECTED_COLUMNS = {
    "olist_orders_dataset.csv": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "olist_customers_dataset.csv": [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ],
    "olist_order_items_dataset.csv": [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
    ],
    "olist_order_payments_dataset.csv": [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value",
    ],
    "olist_order_reviews_dataset.csv": [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp",
    ],
    "olist_products_dataset.csv": [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
    "olist_sellers_dataset.csv": [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state",
    ],
    "olist_geolocation_dataset.csv": [
        "geolocation_zip_code_prefix",
        "geolocation_lat",
        "geolocation_lng",
        "geolocation_city",
        "geolocation_state",
    ],
    "product_category_name_translation.csv": [
        "product_category_name",
        "product_category_name_english",
    ],
}


# --------------------------------------------------
# 3. SAFE READING POLICY
# --------------------------------------------------

# WHY:
# ZIP prefixes are codes, not numeric quantities.
# Reading them as numbers may remove leading zeros.
#
# METHOD:
# Read only these ZIP columns as strings.
#
# IMPORTANT:
# Detailed ZIP format checks belong to Stage 2.

TEXT_COLUMNS = {
    "olist_customers_dataset.csv": {
        "customer_zip_code_prefix": "string",
    },
    "olist_sellers_dataset.csv": {
        "seller_zip_code_prefix": "string",
    },
    "olist_geolocation_dataset.csv": {
        "geolocation_zip_code_prefix": "string",
    },
}


# --------------------------------------------------
# 4. STAGE 1 CHECKLIST
# --------------------------------------------------

# QUESTION:
# Which general profiling checks did we perform?
#
# WHY:
# Readers should understand the scope of this stage.
#
# METHOD:
# Add this checklist to the generated Markdown report.
#
# The script writes the report only after all source
# files have been processed successfully.

GENERAL_CHECKLIST = [
    "- [x] Verify that all nine expected CSV files exist.",
    "- [x] Confirm that all CSV files can be read.",
    "- [x] Calculate the size of each source file.",
    "- [x] Count the rows in every source table.",
    "- [x] Count the columns in every source table.",
    "- [x] List and verify all source column names.",
    "- [x] Record the Pandas dtype of every column.",
    "- [x] Count NULL values in every column.",
    "- [x] Calculate the NULL percentage of every column.",
    "- [x] Count distinct non-NULL values in every column.",
    "- [x] Count exact duplicate rows in every table.",
    "- [x] Generate an overall dataset summary.",
]

ADDITIONAL_CHECKLIST = [
    "- [x] Calculate SHA-256 fingerprints for source files.",
    "- [x] Validate CSV headers and row field counts.",
    "- [x] Verify the expected source column order.",
    "- [x] Protect ZIP prefixes from losing leading zeros.",
]

# The twelve main checklist items are Stage 1 only.
# Stage 2 will study individual column values.
# Stage 3 will study keys and table relationships.
# Stage 4 will document canonical PostgreSQL mapping.


# --------------------------------------------------
# 5. SOURCE FILE FINGERPRINT
# --------------------------------------------------

def sha256_file(path: Path) -> str:
    """Calculate the SHA-256 fingerprint of one source file.

    QUESTION:
    How can we detect if source file bytes change?

    WHY:
    A file name or file size is not enough.

    METHOD:
    Read small binary chunks and calculate a hash.

    NOTE:
    This calculates a fingerprint.
    It does not verify the file against an official hash.
    """

    digest = hashlib.sha256()

    with path.open("rb") as source:
        for chunk in iter(
            lambda: source.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


# --------------------------------------------------
# 6. CSV STRUCTURE VALIDATION
# --------------------------------------------------

def validate_csv_structure(
    path: Path,
    expected_columns: list[str],
) -> int:
    """Check the CSV header and the field count of every row.

    QUESTION:
    Does every CSV row have the expected number of fields?

    WHY:
    A damaged CSV row may cause incorrect reading.

    METHOD:
    Read CSV records and compare their field counts.

    NOTE:
    This is a file structure check.
    It does not test business values.
    """

    try:
        with path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as source:

            reader = csv.reader(
                source,
                strict=True,
            )

            header = next(reader, None)

            if header != expected_columns:
                raise ValueError(
                    f"Unexpected columns in '{path.name}'.\n"
                    f"Expected: {expected_columns}\n"
                    f"Found:    {header}"
                )

            data_rows = 0

            for data_rows, values in enumerate(
                reader,
                start=1,
            ):
                if len(values) != len(expected_columns):
                    raise ValueError(
                        f"CSV record {data_rows} in "
                        f"'{path.name}' has {len(values)} "
                        f"fields; expected "
                        f"{len(expected_columns)}."
                    )

            return data_rows

    except (OSError, UnicodeError, csv.Error) as error:
        raise RuntimeError(
            f"Cannot validate '{path.name}': {error}"
        ) from error


# --------------------------------------------------
# 7. READ A SOURCE FILE
# --------------------------------------------------

def read_source(path: Path) -> pd.DataFrame:
    """Read one original Olist CSV file with Pandas.

    WHY:
    Pandas gives us basic profiling functions.

    METHOD:
    Read the whole CSV and protect ZIP code columns.
    """

    try:
        return pd.read_csv(
            path,
            encoding="utf-8-sig",
            low_memory=False,
            dtype=TEXT_COLUMNS.get(path.name),
            on_bad_lines="error",
        )

    except (
        OSError,
        UnicodeError,
        pd.errors.ParserError,
    ) as error:

        raise RuntimeError(
            f"Cannot read '{path.name}': {error}"
        ) from error


# --------------------------------------------------
# 8. CHECK SOURCE FILE NAMES
# --------------------------------------------------

def check_source_files() -> None:
    """Check that the expected nine CSV files are present.

    WHY:
    We need a complete source dataset before profiling.
    """

    if not SOURCE_DIR.is_dir():
        raise FileNotFoundError(
            f"Source folder not found: {SOURCE_DIR}"
        )

    expected = set(EXPECTED_COLUMNS)

    found = {
        path.name
        for path in SOURCE_DIR.glob("*.csv")
    }

    missing = sorted(expected - found)
    extra = sorted(found - expected)

    if missing or extra:
        raise ValueError(
            f"Source file list changed. "
            f"Missing: {missing}. "
            f"Unexpected: {extra}."
        )


# --------------------------------------------------
# 9. PROFILE ONE COLUMN
# --------------------------------------------------

def column_profile(
    data: pd.DataFrame,
    column: str,
) -> dict:
    """Calculate basic facts for one column.

    QUESTION:
    What is the general condition of this column?

    METHOD:
    Read its dtype, NULL count, NULL rate,
    and number of distinct non-NULL values.

    NOTE:
    We do not decide whether the values are valid here.
    """

    values = data[column]
    row_count = len(data)

    null_count = int(
        values.isna().sum()
    )

    if row_count:
        null_percentage = (
            null_count / row_count * 100
        )
    else:
        null_percentage = 0.0

    return {
        "dtype": str(values.dtype),
        "null_count": null_count,
        "null_pct": null_percentage,
        "distinct_count": int(
            values.nunique(dropna=True)
        ),
    }


# --------------------------------------------------
# 10. PROFILE ALL NINE FILES
# --------------------------------------------------

def profile_sources() -> str:
    """Profile every source CSV and build a Markdown report."""

    # STEP 1:
    # Verify that all expected files exist.
    check_source_files()

    expected_column_count = sum(
        len(columns)
        for columns in EXPECTED_COLUMNS.values()
    )

    if (
        len(EXPECTED_COLUMNS) != 9
        or expected_column_count != 52
    ):
        raise ValueError(
            "Expected source definition must contain "
            "nine files and 52 columns."
        )

    file_rows = []
    column_sections = []

    total_rows = 0
    total_cells = 0
    total_null_cells = 0
    total_duplicate_rows = 0
    total_bytes = 0

    # STEP 2:
    # Profile each file in a stable order.

    for filename, expected_columns in EXPECTED_COLUMNS.items():

        path = SOURCE_DIR / filename

        print(
            f"Reading {filename} ...",
            flush=True,
        )

        # Confirm the CSV structure before profiling.
        csv_row_count = validate_csv_structure(
            path,
            expected_columns,
        )

        # Load the source with Pandas.
        data = read_source(path)

        # Confirm the expected column names and order.
        actual_columns = data.columns.tolist()

        if actual_columns != expected_columns:
            raise ValueError(
                f"Column list changed in '{filename}'.\n"
                f"Expected: {expected_columns}\n"
                f"Found:    {actual_columns}"
            )

        row_count = len(data)

        # Confirm that CSV and Pandas row counts match.
        if csv_row_count != row_count:
            raise ValueError(
                f"Row counts differ in '{filename}': "
                f"{csv_row_count} versus {row_count}."
            )

        column_count = len(actual_columns)
        size_bytes = path.stat().st_size

        # Calculate the source file fingerprint.
        checksum = sha256_file(path)

        # An exact duplicate has the same Pandas-read
        # values in every column of the table.
        #
        # The first row in a repeated group is not counted.
        #
        # We only count repeated rows here.
        # Their meaning belongs to a later research stage.
        duplicate_rows = int(
            data.duplicated(
                keep="first",
            ).sum()
        )

        missing_cells = 0
        detail_rows = []

        # STEP 3:
        # Measure each column in the current file.

        for column in actual_columns:

            stats = column_profile(
                data,
                column,
            )

            missing_cells += stats["null_count"]

            # Explain whether the column was protected
            # as text or read with Pandas type inference.
            if column in TEXT_COLUMNS.get(filename, {}):
                read_policy = "Text (protected ZIP)"
            else:
                read_policy = "Pandas inferred"

            detail_rows.append(
                f"| `{column}` "
                f"| `{stats['dtype']}` "
                f"| {read_policy} "
                f"| {stats['null_count']:,} "
                f"| {stats['null_pct']:.2f}% "
                f"| {stats['distinct_count']:,} |"
            )

        # STEP 4:
        # Add one row to the general file overview.

        file_rows.append(
            f"| `{filename}` "
            f"| {row_count:,} "
            f"| {column_count} "
            f"| {size_bytes:,} "
            f"| {missing_cells:,} "
            f"| {duplicate_rows:,} |"
        )

        # STEP 5:
        # Add a detailed column table for this file.

        column_sections.extend([
            f"### `{filename}`",
            "",
            f"**Rows:** {row_count:,}  ",
            f"**Columns:** {column_count}  ",
            f"**Size (bytes):** {size_bytes:,}  ",
            f"**Exact duplicate rows:** {duplicate_rows:,}  ",
            f"**SHA-256:** `{checksum}`",
            "",
            "| Column | Pandas dtype | Read policy "
            "| NULLs | NULL % | Distinct (not NULL) |",
            "|---|---|---|---:|---:|---:|",
            *detail_rows,
            "",
        ])

        # STEP 6:
        # Update totals across all source files.

        total_rows += row_count
        total_cells += row_count * column_count
        total_null_cells += missing_cells
        total_duplicate_rows += duplicate_rows
        total_bytes += size_bytes

        print(
            f"  {row_count:,} rows "
            f"| {column_count} columns "
            f"| {duplicate_rows:,} duplicate rows"
        )

    # --------------------------------------------------
    # 11. CREATE THE ENGLISH MARKDOWN REPORT
    # --------------------------------------------------

    # The report is created only after all files have
    # been read and profiled successfully.
    #
    # The checklist below documents the checks
    # completed by this successful execution.

    report = [
        "# Olist Source Profile — Stage 1: General Data Profiling",
        "",
        "## Stage 1 — Verification Checklist",
        "",
        "**Status:** 12/12 general profiling checks completed "
        "during this source profiling run.",
        "",
        *GENERAL_CHECKLIST,
        "",
        "### Additional source checks",
        "",
        *ADDITIONAL_CHECKLIST,
        "",
        "**Scope:** This checklist confirms source profiling "
        "operations. It does not mean that all data values "
        "are valid or that production DQ rules are active.",
        "",
        "**SHA-256 note:** Fingerprints were calculated, "
        "but they were not compared with official reference hashes.",
        "",
        "## Question and purpose",
        "",
        "**Question:** What source files, tables, "
        "and columns do we have?",
        "",
        "**Why:** We need basic source facts before "
        "detailed research and database design.",
        "",
        "**Method:** Read all nine Olist CSV files "
        "with Pandas. Measure their size, schema, "
        "row and column counts, Pandas types, "
        "missing values, distinct values, exact "
        "duplicate rows, and SHA-256 fingerprints.",
        "",
        "## Dataset overview",
        "",
        f"- Expected and readable CSV files: "
        f"**{len(EXPECTED_COLUMNS)}**",
        f"- Columns across all files: "
        f"**{expected_column_count}**",
        f"- Rows summed across all files: "
        f"**{total_rows:,}**",
        f"- Total source file bytes: "
        f"**{total_bytes:,}** "
        f"({total_bytes / (1024 ** 2):.2f} MiB)",
        f"- Missing cells across all files: "
        f"**{total_null_cells:,}** "
        f"({(total_null_cells / total_cells * 100) if total_cells else 0:.2f}% of cells)",
        f"- Exact duplicate rows summed across files: "
        f"**{total_duplicate_rows:,}**",
        "",
        "The total row count is a sum of nine different "
        "source tables. It is **not** the number of "
        "unique orders or customers.",
        "",
        "| Source file | Rows | Columns | Bytes "
        "| NULL cells | Exact duplicate rows |",
        "|---|---:|---:|---:|---:|---:|",
        *file_rows,
        "",
        "## Column inventory (all 52 columns)",
        "",
        *column_sections,
        "## How to read this report",
        "",
        "- **Pandas dtype** describes how Pandas "
        "read a column. It is not the final PostgreSQL type.",
        "- **Read policy** shows whether a ZIP prefix "
        "was protected as text or Pandas inferred its type.",
        "- **NULL** uses Pandas default CSV missing-value rules.",
        "- **Distinct** excludes NULL values. "
        "Repeated values are not always errors.",
        "- **Exact duplicate rows** repeat all columns "
        "after Pandas reading. The first copy is not counted. "
        "This does not mean every repeated row is invalid.",
        "- **SHA-256** records source file fingerprints "
        "for future comparisons.",
        "- No business rules, timestamp order checks, "
        "primary-key tests, foreign-key tests, "
        "or JOIN checks are performed here.",
        "",
        "## Next stages (not performed here)",
        "",
        "1. **Detailed Column Analysis:** Meanings, "
        "values, formats, ranges, and special checks.",
        "2. **Key and Relationship Analysis:** Keys, "
        "table grain, links, and JOIN risks.",
        "3. **Canonical Data Mapping:** PostgreSQL "
        "types, source-to-target mappings, "
        "and ingestion design decisions.",
        "",
    ]

    return "\n".join(report)


# --------------------------------------------------
# 12. SAVE THE REPORT
# --------------------------------------------------

def main() -> None:
    """Run the general profiling and save the final report.

    WHY:
    We want a repeatable report, not manual Markdown edits.

    METHOD:
    Run all checks first.
    Write the report only after successful profiling.
    """

    report = profile_sources()

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_FILE.write_text(
        report,
        encoding="utf-8",
    )

    print(
        f"\nStage 1 report saved: {REPORT_FILE}"
    )


if __name__ == "__main__":
    main()
