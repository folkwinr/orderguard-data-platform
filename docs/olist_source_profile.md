# Olist Source Profile — Stage 1: General Data Profiling

## Stage 1 — Verification Checklist

**Status:** 12/12 general profiling checks completed during this source profiling run.

- [x] Verify that all nine expected CSV files exist.
- [x] Confirm that all CSV files can be read.
- [x] Calculate the size of each source file.
- [x] Count the rows in every source table.
- [x] Count the columns in every source table.
- [x] List and verify all source column names.
- [x] Record the Pandas dtype of every column.
- [x] Count NULL values in every column.
- [x] Calculate the NULL percentage of every column.
- [x] Count distinct non-NULL values in every column.
- [x] Count exact duplicate rows in every table.
- [x] Generate an overall dataset summary.

### Additional source checks

- [x] Calculate SHA-256 fingerprints for source files.
- [x] Validate CSV headers and row field counts.
- [x] Verify the expected source column order.
- [x] Protect ZIP prefixes from losing leading zeros.

**Scope:** This checklist confirms source profiling operations. It does not mean that all data values are valid or that production DQ rules are active.

**SHA-256 note:** Fingerprints were calculated, but they were not compared with official reference hashes.

## Question and purpose

**Question:** What source files, tables, and columns do we have?

**Why:** We need basic source facts before detailed research and database design.

**Method:** Read all nine Olist CSV files with Pandas. Measure their size, schema, row and column counts, Pandas types, missing values, distinct values, exact duplicate rows, and SHA-256 fingerprints.

## Dataset overview

- Expected and readable CSV files: **9**
- Columns across all files: **52**
- Rows summed across all files: **1,550,922**
- Total source file bytes: **126,186,995** (120.34 MiB)
- Missing cells across all files: **153,259** (1.78% of cells)
- Exact duplicate rows summed across files: **261,831**

The total row count is a sum of nine different source tables. It is **not** the number of unique orders or customers.

| Source file | Rows | Columns | Bytes | NULL cells | Exact duplicate rows |
|---|---:|---:|---:|---:|---:|
| `olist_orders_dataset.csv` | 99,441 | 8 | 17,654,914 | 4,908 | 0 |
| `olist_customers_dataset.csv` | 99,441 | 5 | 9,033,957 | 0 | 0 |
| `olist_order_items_dataset.csv` | 112,650 | 7 | 15,438,671 | 0 | 0 |
| `olist_order_payments_dataset.csv` | 103,886 | 5 | 5,777,138 | 0 | 0 |
| `olist_order_reviews_dataset.csv` | 99,224 | 7 | 14,451,670 | 145,903 | 0 |
| `olist_products_dataset.csv` | 32,951 | 9 | 2,379,446 | 2,448 | 0 |
| `olist_sellers_dataset.csv` | 3,095 | 4 | 174,703 | 0 | 0 |
| `olist_geolocation_dataset.csv` | 1,000,163 | 5 | 61,273,883 | 0 | 261,831 |
| `product_category_name_translation.csv` | 71 | 2 | 2,613 | 0 | 0 |

## Column inventory (all 52 columns)

### `olist_orders_dataset.csv`

**Rows:** 99,441  
**Columns:** 8  
**Size (bytes):** 17,654,914  
**Exact duplicate rows:** 0  
**SHA-256:** `8df58ef3d2d7e9944010f7beecd9b75367f5588ec6e3c91cec19ae3345ef9ecf`

| Column | Pandas dtype | Read policy | NULLs | NULL % | Distinct (not NULL) |
|---|---|---|---:|---:|---:|
| `order_id` | `str` | Pandas inferred | 0 | 0.00% | 99,441 |
| `customer_id` | `str` | Pandas inferred | 0 | 0.00% | 99,441 |
| `order_status` | `str` | Pandas inferred | 0 | 0.00% | 8 |
| `order_purchase_timestamp` | `str` | Pandas inferred | 0 | 0.00% | 98,875 |
| `order_approved_at` | `str` | Pandas inferred | 160 | 0.16% | 90,733 |
| `order_delivered_carrier_date` | `str` | Pandas inferred | 1,783 | 1.79% | 81,018 |
| `order_delivered_customer_date` | `str` | Pandas inferred | 2,965 | 2.98% | 95,664 |
| `order_estimated_delivery_date` | `str` | Pandas inferred | 0 | 0.00% | 459 |

### `olist_customers_dataset.csv`

**Rows:** 99,441  
**Columns:** 5  
**Size (bytes):** 9,033,957  
**Exact duplicate rows:** 0  
**SHA-256:** `983a422239e1712ded753b3bf9ecf47dc73f144d306029dcfa99e70a226883d2`

| Column | Pandas dtype | Read policy | NULLs | NULL % | Distinct (not NULL) |
|---|---|---|---:|---:|---:|
| `customer_id` | `str` | Pandas inferred | 0 | 0.00% | 99,441 |
| `customer_unique_id` | `str` | Pandas inferred | 0 | 0.00% | 96,096 |
| `customer_zip_code_prefix` | `string` | Text (protected ZIP) | 0 | 0.00% | 14,994 |
| `customer_city` | `str` | Pandas inferred | 0 | 0.00% | 4,119 |
| `customer_state` | `str` | Pandas inferred | 0 | 0.00% | 27 |

### `olist_order_items_dataset.csv`

**Rows:** 112,650  
**Columns:** 7  
**Size (bytes):** 15,438,671  
**Exact duplicate rows:** 0  
**SHA-256:** `0bc4d068c4fe38cbb01bd90e8746e3c613fe7b4baef75fab7b0e329701c3e279`

| Column | Pandas dtype | Read policy | NULLs | NULL % | Distinct (not NULL) |
|---|---|---|---:|---:|---:|
| `order_id` | `str` | Pandas inferred | 0 | 0.00% | 98,666 |
| `order_item_id` | `int64` | Pandas inferred | 0 | 0.00% | 21 |
| `product_id` | `str` | Pandas inferred | 0 | 0.00% | 32,951 |
| `seller_id` | `str` | Pandas inferred | 0 | 0.00% | 3,095 |
| `shipping_limit_date` | `str` | Pandas inferred | 0 | 0.00% | 93,318 |
| `price` | `float64` | Pandas inferred | 0 | 0.00% | 5,968 |
| `freight_value` | `float64` | Pandas inferred | 0 | 0.00% | 6,999 |

### `olist_order_payments_dataset.csv`

**Rows:** 103,886  
**Columns:** 5  
**Size (bytes):** 5,777,138  
**Exact duplicate rows:** 0  
**SHA-256:** `4f713964f2815dbbaa40b9488268c55aac3627bfce5aa96cf58d1f3616de3cc0`

| Column | Pandas dtype | Read policy | NULLs | NULL % | Distinct (not NULL) |
|---|---|---|---:|---:|---:|
| `order_id` | `str` | Pandas inferred | 0 | 0.00% | 99,440 |
| `payment_sequential` | `int64` | Pandas inferred | 0 | 0.00% | 29 |
| `payment_type` | `str` | Pandas inferred | 0 | 0.00% | 5 |
| `payment_installments` | `int64` | Pandas inferred | 0 | 0.00% | 24 |
| `payment_value` | `float64` | Pandas inferred | 0 | 0.00% | 29,077 |

### `olist_order_reviews_dataset.csv`

**Rows:** 99,224  
**Columns:** 7  
**Size (bytes):** 14,451,670  
**Exact duplicate rows:** 0  
**SHA-256:** `012b61c7593e34f51fa614efdf802b9c7056ce6aae5307ddb93236e7cfc797d7`

| Column | Pandas dtype | Read policy | NULLs | NULL % | Distinct (not NULL) |
|---|---|---|---:|---:|---:|
| `review_id` | `str` | Pandas inferred | 0 | 0.00% | 98,410 |
| `order_id` | `str` | Pandas inferred | 0 | 0.00% | 98,673 |
| `review_score` | `int64` | Pandas inferred | 0 | 0.00% | 5 |
| `review_comment_title` | `str` | Pandas inferred | 87,656 | 88.34% | 4,527 |
| `review_comment_message` | `str` | Pandas inferred | 58,247 | 58.70% | 36,159 |
| `review_creation_date` | `str` | Pandas inferred | 0 | 0.00% | 636 |
| `review_answer_timestamp` | `str` | Pandas inferred | 0 | 0.00% | 98,248 |

### `olist_products_dataset.csv`

**Rows:** 32,951  
**Columns:** 9  
**Size (bytes):** 2,379,446  
**Exact duplicate rows:** 0  
**SHA-256:** `3e6569628a17fbc75fd206ee357b59e20364b9afa90f5b6cd5b4d624c58aa9cc`

| Column | Pandas dtype | Read policy | NULLs | NULL % | Distinct (not NULL) |
|---|---|---|---:|---:|---:|
| `product_id` | `str` | Pandas inferred | 0 | 0.00% | 32,951 |
| `product_category_name` | `str` | Pandas inferred | 610 | 1.85% | 73 |
| `product_name_lenght` | `float64` | Pandas inferred | 610 | 1.85% | 66 |
| `product_description_lenght` | `float64` | Pandas inferred | 610 | 1.85% | 2,960 |
| `product_photos_qty` | `float64` | Pandas inferred | 610 | 1.85% | 19 |
| `product_weight_g` | `float64` | Pandas inferred | 2 | 0.01% | 2,204 |
| `product_length_cm` | `float64` | Pandas inferred | 2 | 0.01% | 99 |
| `product_height_cm` | `float64` | Pandas inferred | 2 | 0.01% | 102 |
| `product_width_cm` | `float64` | Pandas inferred | 2 | 0.01% | 95 |

### `olist_sellers_dataset.csv`

**Rows:** 3,095  
**Columns:** 4  
**Size (bytes):** 174,703  
**Exact duplicate rows:** 0  
**SHA-256:** `1f643d2b950373b85735e7794b20986f528d7a000432e7c6f9bcbb44d0846a0e`

| Column | Pandas dtype | Read policy | NULLs | NULL % | Distinct (not NULL) |
|---|---|---|---:|---:|---:|
| `seller_id` | `str` | Pandas inferred | 0 | 0.00% | 3,095 |
| `seller_zip_code_prefix` | `string` | Text (protected ZIP) | 0 | 0.00% | 2,246 |
| `seller_city` | `str` | Pandas inferred | 0 | 0.00% | 611 |
| `seller_state` | `str` | Pandas inferred | 0 | 0.00% | 23 |

### `olist_geolocation_dataset.csv`

**Rows:** 1,000,163  
**Columns:** 5  
**Size (bytes):** 61,273,883  
**Exact duplicate rows:** 261,831  
**SHA-256:** `b514f6fc991b9566aeba02aa5d67e2c3630f034b60a0e05aa0d082a3b66d88d6`

| Column | Pandas dtype | Read policy | NULLs | NULL % | Distinct (not NULL) |
|---|---|---|---:|---:|---:|
| `geolocation_zip_code_prefix` | `string` | Text (protected ZIP) | 0 | 0.00% | 19,015 |
| `geolocation_lat` | `float64` | Pandas inferred | 0 | 0.00% | 717,360 |
| `geolocation_lng` | `float64` | Pandas inferred | 0 | 0.00% | 717,613 |
| `geolocation_city` | `str` | Pandas inferred | 0 | 0.00% | 8,011 |
| `geolocation_state` | `str` | Pandas inferred | 0 | 0.00% | 27 |

### `product_category_name_translation.csv`

**Rows:** 71  
**Columns:** 2  
**Size (bytes):** 2,613  
**Exact duplicate rows:** 0  
**SHA-256:** `a81f0d1f27b27e7293f761bc79e3ce8f348ee39c4b3ed3e49bde38f478586278`

| Column | Pandas dtype | Read policy | NULLs | NULL % | Distinct (not NULL) |
|---|---|---|---:|---:|---:|
| `product_category_name` | `str` | Pandas inferred | 0 | 0.00% | 71 |
| `product_category_name_english` | `str` | Pandas inferred | 0 | 0.00% | 71 |

## How to read this report

- **Pandas dtype** describes how Pandas read a column. It is not the final PostgreSQL type.
- **Read policy** shows whether a ZIP prefix was protected as text or Pandas inferred its type.
- **NULL** uses Pandas default CSV missing-value rules.
- **Distinct** excludes NULL values. Repeated values are not always errors.
- **Exact duplicate rows** repeat all columns after Pandas reading. The first copy is not counted. This does not mean every repeated row is invalid.
- **SHA-256** records source file fingerprints for future comparisons.
- No business rules, timestamp order checks, primary-key tests, foreign-key tests, or JOIN checks are performed here.

## Next stages (not performed here)

1. **Detailed Column Analysis:** Meanings, values, formats, ranges, and special checks.
2. **Key and Relationship Analysis:** Keys, table grain, links, and JOIN risks.
3. **Canonical Data Mapping:** PostgreSQL types, source-to-target mappings, and ingestion design decisions.
