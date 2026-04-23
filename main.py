import time
from src.spark_session import get_spark
from src.bronze import process_bronze
from src.silver import process_silver
from src.gold import process_gold

def run_pipeline():
    print("==================================================")
    print("🚀 INITIALIZING NYC TAXI DATA PIPELINE 🚀")
    print("==================================================")
    
    start_time = time.time()
    
    # Boot up the engine once for the whole pipeline
    spark = get_spark()
    
    try:
        # Step 1: Ingestion
        process_bronze(spark)
        
        # Step 2: Cleansing
        process_silver(spark)
        
        # Step 3: Modeling
        process_gold(spark)
        
        # Step 4: Query and Display Results
        print("--- Running Analysis Query ---")
        run_query(spark)
        
        print("==================================================")
        print("✅ PIPELINE COMPLETED SUCCESSFULLY ✅")
        
    except Exception as e:
        print("==================================================")
        print("❌ PIPELINE FAILED ❌")
        print(f"Error: {e}")
        
    finally:
        # Calculate execution time
        end_time = time.time()
        elapsed_minutes = (end_time - start_time) / 60
        print(f"⏱️ Total Execution Time: {elapsed_minutes:.2f} minutes")
        print("==================================================")
        
        # Always tear down the cluster
        spark.stop()

def run_query(spark):
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

if __name__ == "__main__":
    run_pipeline()