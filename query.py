from src.spark_session import get_spark

spark = get_spark()

# 1. Load the Gold Parquet files
fact_df = spark.read.parquet("data/gold/fact_trips")
dim_date_df = spark.read.parquet("data/gold/dim_date")

# 2. Register them as temporary SQL tables
fact_df.createOrReplaceTempView("fact_trips")
dim_date_df.createOrReplaceTempView("dim_date")

# 3. Write standard SQL!
query = """
    SELECT 
        d.day_of_week,
        COUNT(*) as total_trips,
        ROUND(AVG(f.total_amount), 2) as avg_fare,
        ROUND(SUM(f.tip_amount), 2) as total_tips
    FROM fact_trips f
    JOIN dim_date d ON f.pickup_datetime = d.datetime
    GROUP BY d.day_of_week
    ORDER BY total_trips DESC
"""

print("Executing SQL Query against Parquet files...")
result = spark.sql(query)
result.show()

spark.stop()