from pyspark.sql import SparkSession
import os
import sys

def get_spark():
    # Fix for Windows PySpark HADOOP_HOME and DLL errors
    if sys.platform.startswith('win'):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        hadoop_home = os.path.join(project_root, 'hadoop')
        hadoop_bin = os.path.join(hadoop_home, 'bin')
        
        # 1. Set HADOOP_HOME
        os.environ['HADOOP_HOME'] = hadoop_home
        
        # 2. CRITICAL FIX: Add the bin folder to the Windows PATH so Java finds hadoop.dll
        os.environ['PATH'] = hadoop_bin + os.pathsep + os.environ.get('PATH', '')

    # Create the Spark Session
    spark = (SparkSession.builder 
            .appName("NYCTaxiPipeline") 
            .master("local[*]") 
            .config("spark.driver.memory", "4g") 
            .config("spark.executor.memory", "4g")
            .getOrCreate())
    
    # Silence the annoying warning logs
    spark.sparkContext.setLogLevel("ERROR") 
    
    return spark