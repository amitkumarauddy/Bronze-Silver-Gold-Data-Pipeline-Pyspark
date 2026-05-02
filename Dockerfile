FROM python:3.12-slim-bookworm

WORKDIR /app

# Install Java (required for PySpark)
RUN apt-get update && apt-get install -y default-jre && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Install only Python dependencies first for better layer caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application code, not the data folder
COPY main.py /app/
COPY src/ /app/src/

CMD ["python", "main.py"]