import os

# Get the absolute path to the root of our project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define all our data paths in one single place
RAW_DATA_PATH = os.path.join(ROOT_DIR, "data", "raw")
BRONZE_DATA_PATH = os.path.join(ROOT_DIR, "data", "bronze")
SILVER_DATA_PATH = os.path.join(ROOT_DIR, "data", "silver")
GOLD_DATA_PATH = os.path.join(ROOT_DIR, "data", "gold")

# We can also store pipeline configurations here
SPARK_DRIVER_MEMORY = "4g"
SPARK_EXECUTOR_MEMORY = "4g"