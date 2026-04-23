from pyspark.sql.functions import col, year, month, dayofmonth, hour, dayofweek
import os

# Import centralized paths
from src.config import SILVER_DATA_PATH, GOLD_DATA_PATH

def process_gold(spark):
    print("--- Starting Gold Layer Processing ---")
    
    # 1. Read the clean Silver data
    print("Reading clean Silver data...")
    df = spark.read.parquet(SILVER_DATA_PATH)

    # ==========================================
    # 2. CREATE DIMENSION: dim_date
    # ==========================================
    print("Building dim_date...")
    # Extract unique pickup and dropoff times
    pickup_times = df.select(col("tpep_pickup_datetime").alias("datetime"))
    dropoff_times = df.select(col("tpep_dropoff_datetime").alias("datetime"))
    
    unique_times = pickup_times.union(dropoff_times).distinct()

    dim_date = (unique_times
        .withColumn("year", year("datetime"))
        .withColumn("month", month("datetime"))
        .withColumn("day", dayofmonth("datetime"))
        .withColumn("hour", hour("datetime"))
        .withColumn("day_of_week", dayofweek("datetime")) 
    )

    # ==========================================
    # 3. CREATE FACT: fact_trips
    # ==========================================
    print("Building fact_trips...")
    fact_trips = df.select(
        col("tpep_pickup_datetime").alias("pickup_datetime"), 
        col("tpep_dropoff_datetime").alias("dropoff_datetime"), 
        col("PULocationID").alias("pickup_location_id"),
        col("DOLocationID").alias("dropoff_location_id"),
        col("passenger_count"),
        col("trip_distance"),
        col("fare_amount"),
        col("tip_amount"),
        col("total_amount")
    )

    # ==========================================
    # 4. WRITE TO GOLD LAYER
    # ==========================================
    print(f"Writing Gold tables to {GOLD_DATA_PATH}...")
    
    # Save the Dimension inside the Gold folder
    (dim_date.write
        .mode("overwrite")
        .parquet(os.path.join(GOLD_DATA_PATH, "dim_date")))

    # Save the Fact inside the Gold folder
    (fact_trips.write
        .mode("overwrite")
        .parquet(os.path.join(GOLD_DATA_PATH, "fact_trips")))

    print("--- Gold Layer Complete! ---\n")

if __name__ == "__main__":
    from spark_session import get_spark
    spark = get_spark()
    process_gold(spark)
    spark.stop()