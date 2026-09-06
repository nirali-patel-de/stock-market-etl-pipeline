import duckdb

PARQUET_FILE = "data/processed/stock_market.parquet"

con = duckdb.connect("data/processed/stock_market.duckdb")

print("DuckDB connected successfully.\n")

# 1. Dataset overview
print("=== DATASET OVERVIEW ===")

overview = con.execute(
    f"""
    SELECT
        COUNT(*) AS total_records,
        COUNT(DISTINCT Ticker) AS total_stocks,
        MIN(Date) AS start_date,
        MAX(Date) AS end_date
    FROM read_parquet('{PARQUET_FILE}')
    """
).fetchdf()

print(overview)

# 2. Records per stock
print("\n=== RECORDS PER STOCK ===")

records = con.execute(
    f"""
    SELECT
        Ticker,
        COUNT(*) AS total_records,
        MIN(Date) AS start_date,
        MAX(Date) AS end_date
    FROM read_parquet('{PARQUET_FILE}')
    GROUP BY Ticker
    ORDER BY Ticker
    """
).fetchdf()

print(records)

# 3. Basic price statistics
print("\n=== PRICE STATISTICS ===")

stats = con.execute(
    f"""
    SELECT
        Ticker,
        ROUND(MIN(Low), 2) AS lowest_price,
        ROUND(MAX(High), 2) AS highest_price,
        ROUND(AVG(Close), 2) AS average_close,
        ROUND(AVG(Volume), 0) AS average_volume
    FROM read_parquet('{PARQUET_FILE}')
    GROUP BY Ticker
    ORDER BY Ticker
    """
).fetchdf()

print(stats)

# 4. Calculate daily returns
print("\n=== DAILY RETURNS ===")

daily_returns = con.execute(
    f"""
    SELECT
        Ticker,
        Date,
        ROUND(Close - Open, 2) AS daily_return
    FROM read_parquet('{PARQUET_FILE}')
    WHERE Date = (SELECT MAX(Date)
                FROM read_parquet('{PARQUET_FILE}'))
    """
).fetchdf()

print(daily_returns)

# 5. Analyze price performance
print("\n=== PRICE PERFORMANCE ===")

price_perf = con.execute(
    f"""
    WITH ranked_prices AS (
    SELECT
        Ticker,
        Date,
        Open,
        High,
        Low,
        Close,

        ROW_NUMBER() OVER (
            PARTITION BY Ticker
            ORDER BY Date
        ) AS first_day,

        ROW_NUMBER() OVER (
            PARTITION BY Ticker
            ORDER BY Date DESC
        ) AS last_day

    FROM read_parquet('{PARQUET_FILE}')
    ),

    price_performance AS (
    SELECT
        Ticker,

        MAX(CASE WHEN first_day = 1 THEN Date END) AS start_date,
        MAX(CASE WHEN first_day = 1 THEN Close END) AS start_price,

        MAX(CASE WHEN last_day = 1 THEN Date END) AS end_date,
        MAX(CASE WHEN last_day = 1 THEN Close END) AS end_price,

        MAX(High) AS highest_price,
        MIN(Low) AS lowest_price,

        AVG(Close) AS average_close

    FROM ranked_prices
    GROUP BY Ticker
    )

    SELECT
        Ticker,
        start_date,
        ROUND(start_price, 2) AS start_price,
        end_date,
        ROUND(end_price, 2) AS end_price,

        ROUND(end_price - start_price, 2) AS price_change,

        ROUND(
            ((end_price - start_price) / start_price) * 100,
            2
        ) AS price_change_pct,

        ROUND(highest_price, 2) AS highest_price,
        ROUND(lowest_price, 2) AS lowest_price,
        ROUND(average_close, 2) AS average_close

    FROM price_performance
    ORDER BY price_change_pct DESC
    """
).fetchdf()

print(price_perf)

# 6. Analyze trading volume
print("\n=== TRADING VOLUME ===")

trading_volume = con.execute(
    f"""
    SELECT
        Ticker,
        ROUND(AVG(Volume), 0) AS average_volume,
        MAX(Volume) AS highest_volume,
        MIN(Volume) AS lowest_volume,
        SUM(Volume) AS total_volume
    FROM read_parquet('{PARQUET_FILE}')
    GROUP BY Ticker
    ORDER BY average_volume DESC
    """
).fetchdf()

print(trading_volume)

con.close()