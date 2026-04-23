from pyspark.sql.functions import current_timestamp
from tqdm import tqdm
import os
import shutil

# Import centralized paths
from src.config import RAW_DATA_PATH, BRONZE_DATA_PATH

def process_bronze(spark):
    print("--- Starting Bronze Layer Ingestion ---")
    
    # Safely clear the bronze folder if we are re-running
    if os.path.exists(BRONZE_DATA_PATH):
        shutil.rmtree(BRONZE_DATA_PATH) 

    # Get a list of only the .parquet files in the raw folder
    files = [f for f in os.listdir(RAW_DATA_PATH) if f.endswith('.parquet')]
    
    if not files:
        print(f"Error: No parquet files found in {RAW_DATA_PATH}")
        return

    print(f"Found {len(files)} files. Processing in batches to save RAM...")

    # Wrap our file list in tqdm() to generate the progress bar
    for file in tqdm(files, desc="Processing Taxi Data", unit="file", colour="green"):
        file_path = os.path.join(RAW_DATA_PATH, file)

        # 1. Read ONE file at a time
        df = spark.read.parquet(file_path)

        # 2. Add metadata
        bronze_df = df.withColumn("ingestion_timestamp", current_timestamp())

        # 3. Write to Bronze
        (bronze_df.write
            .mode("append") 
            .parquet(BRONZE_DATA_PATH))
    
    # Read the final appended folder just to get a final row count
    final_count = spark.read.parquet(BRONZE_DATA_PATH).count()
    print(f"\n--- Bronze Layer Complete! Total Rows: {final_count} ---")

if __name__ == "__main__":
    from spark_session import get_spark
    spark = get_spark()
    process_bronze(spark)
    # Safe to stop the spark session here because this block only runs if executed directly
    spark.stop()