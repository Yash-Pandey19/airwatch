FROM apache/airflow:latest-python3.8

# Add local pip binaries to PATH
ENV PATH="/home/airflow/.local/bin:$PATH"

COPY ./pip-chill-requirements.txt .
RUN pip install --no-cache-dir -r pip-chill-requirements.txt

