# Noon UAE — Synthetic Sales Dataset & Streamlit Dashboard

A 3-month (Apr 1 – Jun 30, 2026), order-level **synthetic** e-commerce dataset styled after
a UAE marketplace like Noon, plus a ready-to-run Streamlit dashboard to explore it.

> ⚠️ **This is fabricated demo data**, generated for portfolio/learning purposes. It is not
> real Noon.com data and should not be used to make business claims about Noon.

## What's in this repo

| File | Description |
|---|---|
| `generate_noon_uae_data.ipynb` | Jupyter notebook that generates the dataset from scratch and saves it to CSV |
| `noon_uae_sales_data.csv` | The generated dataset (6,000 orders) |
| `app.py` | Streamlit dashboard that visualizes the dataset |
| `requirements.txt` | Python dependencies |

## Dataset schema

| Column | Type | Description |
|---|---|---|
| `order_id` | string | Unique order identifier |
| `order_date` | datetime | Timestamp of the order |
| `customer_id` | string | Anonymized customer identifier |
| `city` | string | UAE city (Dubai, Abu Dhabi, Sharjah, Ajman, RAK, Fujairah, UAQ, Al Ain) |
| `category` | string | Product category (10 categories) |
| `brand` | string | Brand within the category |
| `unit_price_aed` | float | Price per unit in AED |
| `quantity` | int | Units ordered |
| `discount_percent` | int | Discount applied |
| `total_amount_aed` | float | `unit_price_aed * quantity * (1 - discount_percent/100)` |
| `payment_method` | string | Cash on Delivery, Credit/Debit Card, Noon Pay Later, Apple Pay |
| `device_type` | string | Mobile App, Mobile Web, Desktop |
| `delivery_status` | string | Delivered, In Transit, Cancelled, Returned |
| `delivery_days` | float | Days to deliver (only for delivered orders) |
| `is_noon_vip` | bool | Whether the customer is a VIP/subscription member |
| `customer_rating` | float | 1–5 star rating (only for delivered orders) |

## Regenerating the dataset

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace generate_noon_uae_data.ipynb
```

This overwrites `noon_uae_sales_data.csv`. Change `N` (row count) or the `start_date`/`end_date`
in the notebook to resize or re-date the dataset. The random seed is fixed (`42`) so re-running
without changes reproduces the same data.

## Running the dashboard locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## Deploying to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in, and click **New app**.
3. Point it at your repo, branch `main`, and file `app.py`.
4. Deploy — Streamlit Cloud installs `requirements.txt` automatically.

## License

Free to use for demos, learning, and portfolios.
