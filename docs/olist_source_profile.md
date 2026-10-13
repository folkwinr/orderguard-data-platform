# Olist Source Data Profile

Generated from the original Olist CSV files.
Raw source files are not modified.

Pandas data types are inferred from source values.
They are not final PostgreSQL column definitions.

## olist_customers_dataset.csv

- Rows: 99,441
- Columns: 5

| Column | Pandas dtype | Missing | Missing % |
|---|---|---:|---:|
| `customer_id` | `str` | 0 | 0.00% |
| `customer_unique_id` | `str` | 0 | 0.00% |
| `customer_zip_code_prefix` | `int64` | 0 | 0.00% |
| `customer_city` | `str` | 0 | 0.00% |
| `customer_state` | `str` | 0 | 0.00% |

## olist_geolocation_dataset.csv

- Rows: 1,000,163
- Columns: 5

| Column | Pandas dtype | Missing | Missing % |
|---|---|---:|---:|
| `geolocation_zip_code_prefix` | `int64` | 0 | 0.00% |
| `geolocation_lat` | `float64` | 0 | 0.00% |
| `geolocation_lng` | `float64` | 0 | 0.00% |
| `geolocation_city` | `str` | 0 | 0.00% |
| `geolocation_state` | `str` | 0 | 0.00% |

## olist_order_items_dataset.csv

- Rows: 112,650
- Columns: 7

| Column | Pandas dtype | Missing | Missing % |
|---|---|---:|---:|
| `order_id` | `str` | 0 | 0.00% |
| `order_item_id` | `int64` | 0 | 0.00% |
| `product_id` | `str` | 0 | 0.00% |
| `seller_id` | `str` | 0 | 0.00% |
| `shipping_limit_date` | `str` | 0 | 0.00% |
| `price` | `float64` | 0 | 0.00% |
| `freight_value` | `float64` | 0 | 0.00% |

## olist_order_payments_dataset.csv

- Rows: 103,886
- Columns: 5

| Column | Pandas dtype | Missing | Missing % |
|---|---|---:|---:|
| `order_id` | `str` | 0 | 0.00% |
| `payment_sequential` | `int64` | 0 | 0.00% |
| `payment_type` | `str` | 0 | 0.00% |
| `payment_installments` | `int64` | 0 | 0.00% |
| `payment_value` | `float64` | 0 | 0.00% |

## olist_order_reviews_dataset.csv

- Rows: 99,224
- Columns: 7

| Column | Pandas dtype | Missing | Missing % |
|---|---|---:|---:|
| `review_id` | `str` | 0 | 0.00% |
| `order_id` | `str` | 0 | 0.00% |
| `review_score` | `int64` | 0 | 0.00% |
| `review_comment_title` | `str` | 87,656 | 88.34% |
| `review_comment_message` | `str` | 58,247 | 58.70% |
| `review_creation_date` | `str` | 0 | 0.00% |
| `review_answer_timestamp` | `str` | 0 | 0.00% |

## olist_orders_dataset.csv

- Rows: 99,441
- Columns: 8

| Column | Pandas dtype | Missing | Missing % |
|---|---|---:|---:|
| `order_id` | `str` | 0 | 0.00% |
| `customer_id` | `str` | 0 | 0.00% |
| `order_status` | `str` | 0 | 0.00% |
| `order_purchase_timestamp` | `str` | 0 | 0.00% |
| `order_approved_at` | `str` | 160 | 0.16% |
| `order_delivered_carrier_date` | `str` | 1,783 | 1.79% |
| `order_delivered_customer_date` | `str` | 2,965 | 2.98% |
| `order_estimated_delivery_date` | `str` | 0 | 0.00% |

## olist_products_dataset.csv

- Rows: 32,951
- Columns: 9

| Column | Pandas dtype | Missing | Missing % |
|---|---|---:|---:|
| `product_id` | `str` | 0 | 0.00% |
| `product_category_name` | `str` | 610 | 1.85% |
| `product_name_lenght` | `float64` | 610 | 1.85% |
| `product_description_lenght` | `float64` | 610 | 1.85% |
| `product_photos_qty` | `float64` | 610 | 1.85% |
| `product_weight_g` | `float64` | 2 | 0.01% |
| `product_length_cm` | `float64` | 2 | 0.01% |
| `product_height_cm` | `float64` | 2 | 0.01% |
| `product_width_cm` | `float64` | 2 | 0.01% |

## olist_sellers_dataset.csv

- Rows: 3,095
- Columns: 4

| Column | Pandas dtype | Missing | Missing % |
|---|---|---:|---:|
| `seller_id` | `str` | 0 | 0.00% |
| `seller_zip_code_prefix` | `int64` | 0 | 0.00% |
| `seller_city` | `str` | 0 | 0.00% |
| `seller_state` | `str` | 0 | 0.00% |

## product_category_name_translation.csv

- Rows: 71
- Columns: 2

| Column | Pandas dtype | Missing | Missing % |
|---|---|---:|---:|
| `product_category_name` | `str` | 0 | 0.00% |
| `product_category_name_english` | `str` | 0 | 0.00% |

## Key Checks

| Check | Count |
|---|---:|
| Duplicate order IDs | 0 |
| Duplicate customer IDs | 0 |
| Duplicate order item keys | 0 |
| Duplicate product IDs | 0 |
| Duplicate seller IDs | 0 |
| Duplicate payment keys | 0 |
| Missing order IDs | 0 |
| Missing customer IDs | 0 |
| Missing order item IDs | 0 |
| Missing product IDs | 0 |
| Missing seller IDs | 0 |

## Referential Integrity Checks

| Check | Count |
|---|---:|
| Orders without a matching customer | 0 |
| Customers without a matching order | 0 |
| Order items without a matching order | 0 |
| Order items without a matching product | 0 |
| Order items without a matching seller | 0 |
| Payments without a matching order | 0 |
| Reviews without a matching order | 0 |
| Products with unmatched non-null categories | 13 |

## Descriptive Findings

| Check | Count |
|---|---:|
| Orders without order items | 775 |
| Orders without payments | 1 |
| Orders without reviews | 768 |
| Unique customers | 96,096 |
| Customers with multiple customer records | 2,997 |
| Delivered orders without a delivery date | 8 |

## Orders Without Items by Status

| Order status | Orders |
|---|---:|
| `unavailable` | 603 |
| `canceled` | 164 |
| `created` | 5 |
| `invoiced` | 2 |
| `shipped` | 1 |

## Orders Without Payment Records

| Order ID | Status | Approved At | Delivered At |
|---|---|---|---|
| `bfbd0f9bdef84302105ad712db648a6c` | `delivered` | 2016-09-15 12:16:38 | 2016-11-09 07:47:38 |

## Unmatched Product Categories

| Original category | Product records |
|---|---:|
| `portateis_cozinha_e_preparadores_de_alimentos` | 10 |
| `pc_gamer` | 3 |

## Relationship Cardinality

| Child table | Distinct orders | Orders with multiple rows | Maximum rows per order |
|---|---:|---:|---:|
| Order items | 98,666 | 9,803 | 21 |
| Payments | 99,440 | 2,961 | 29 |
| Reviews | 98,673 | 547 | 3 |

## Interpretation Notes

- These are source profiling results, not final quality verdicts.
- Orders without items may be explained by their status.
- A delivered order without a payment record requires investigation.
- Missing category translations require reference data handling.
- Missing reviews do not automatically indicate invalid orders.
- Referential checks exclude null child keys; missingness is reported separately.
- Geolocation ZIP prefixes are not unique primary keys.
- ZIP code prefixes should be represented as text in the target schema.
- Original CSV files are not modified.
- No PostgreSQL ingestion or quarantine actions are performed by this script.

