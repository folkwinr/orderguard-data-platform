# Olist Source Data Profile

This report is generated from the original Olist CSV files.
Raw source files are not modified.

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

## Key and Relationship Checks

| Check | Count |
|---|---:|
| Duplicate order IDs | 0 |
| Duplicate customer IDs | 0 |
| Duplicate order item keys | 0 |
| Orders without a matching customer | 0 |
| Order items without a matching order | 0 |
| Orders without order items | 775 |

