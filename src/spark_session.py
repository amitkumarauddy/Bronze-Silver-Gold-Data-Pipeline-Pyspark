from pyspark.sql import SparkSession
import os
import sys
import shutil


def _find_java_home():
    java_path = shutil.which("java")
    if not java_path:
        return None

    java_real = os.path.realpath(java_path)
    java_home = os.path.dirname(os.path.dirname(java_real))
    return java_home if os.path.exists(java_home) else None


def _ensure_java_home():
    if os.environ.get("JAVA_HOME"):
        return

    java_home = _find_java_home()
    if java_home:
        os.environ["JAVA_HOME"] = java_home
        return

    raise EnvironmentError(
        "JAVA_HOME is not set and Java was not found in PATH. "
        "Install Java 8, 11, or 17 and set JAVA_HOME before running the pipeline. "
        "Example on Linux:\n"
        "  sudo apt install openjdk-17-jdk\n"
        "  export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64\n"
        "  export PATH=\"$JAVA_HOME/bin:$PATH\"\n"
        "Then run: python main.py"
    )


def get_spark():
    _ensure_java_home()

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