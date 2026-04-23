from pyspark.sql.functions import col
import os

# Import centralized paths
from src.config import BRONZE_DATA_PATH, SILVER_DATA_PATH

def process_silver(spark):
    print("--- Starting Silver Layer Processing ---")
    
    # 1. Read the raw bronze data
    print("Reading Bronze data...")
    df = spark.read.parquet(BRONZE_DATA_PATH)
    initial_count = df.count()
    print(f"Rows before cleaning: {initial_count}")

    # 2. Drop exact duplicates
    df_dedup = df.dropDuplicates()

    # 3. Filter out business anomalies
    print("Applying business logic filters...")
    df_clean = df_dedup.filter(
        (col("passenger_count") > 0) &
        (col("trip_distance") > 0.0) &
        (col("total_amount") > 0.0)
    )

    # Calculate how much garbage we threw out
    final_count = df_clean.count()
    print(f"Rows after cleaning: {final_count}")
    print(f"Total garbage rows removed: {initial_count - final_count}")

    # 4. Write to the Silver layer
    print(f"Writing clean data to {SILVER_DATA_PATH}...")
    (df_clean.write
        .mode("overwrite") 
        .parquet(SILVER_DATA_PATH))
    
    print("--- Silver Layer Complete! ---\n")

if __name__ == "__main__":
    from spark_session import get_spark
    spark = get_spark()
    process_silver(spark)
    spark.stop()