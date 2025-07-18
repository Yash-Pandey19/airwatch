# Airflow Data Pipeline with Great Expectations

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.x-green.svg)](https://airflow.apache.org/)
[![Great Expectations](https://img.shields.io/badge/Great%20Expectations-0.15+-red.svg)](https://greatexpectations.io/)
[![Docker](https://img.shields.io/badge/Docker-enabled-blue.svg)](https://www.docker.com/)

A production-ready data pipeline built with Apache Airflow that integrates Great Expectations for comprehensive data validation and quality assurance. This project demonstrates how to build robust ETL pipelines with automated data quality checks at every stage.

## 🚀 Overview

This project implements a complete data pipeline for retail e-commerce data processing with the following key features:

- **ETL Pipeline**: Extract, Transform, and Load retail data through multiple stages
- **Data Validation**: Comprehensive data quality checks using Great Expectations
- **Containerized Deployment**: Docker-based setup for easy deployment and scalability
- **Multi-Database Architecture**: Separate PostgreSQL databases for source, destination, and data store
- **Email Alerts**: Automated notifications for pipeline failures and data quality issues
- **Monitoring**: Built-in logging and error tracking

## 🏗️ Architecture

![Airflow GeX Data Pipeline Architecture](Airflow%20GeX%20Data%20Pipeline.webp)

### Pipeline Stages

1. **Source Data Validation** - Validate raw data quality before processing
2. **Data Extraction** - Extract data from source database to filesystem
3. **Raw Data Validation** - Validate extracted data format and completeness
4. **Data Transformation** - Clean and transform data (remove nulls, type conversion)
5. **Stage Data Validation** - Validate transformed data quality
6. **Data Loading** - Load processed data into destination warehouse
7. **Warehouse Validation** - Final validation of loaded data

## 📁 Project Structure

```
.
├── dags/                           # Airflow DAGs and scripts
│   ├── scripts/
│   │   ├── python/                 # Python transformation scripts
│   │   │   ├── retail_dest.py
│   │   │   ├── retail_load.py
│   │   │   ├── retail_source.py
│   │   │   ├── retail_transform.py
│   │   │   ├── retail_warehouse.py
│   │   │   └── utils.py
│   │   └── sql/                    # SQL scripts for data operations
│   │       ├── extract_json_column.sql
│   │       ├── extract_load_retail_source.sql
│   │       ├── load_retail_stage.sql
│   │       └── transform_load_retail_warehouse.sql
│   ├── retail_data_pipeline.py     # Main Airflow DAG
│   └── transformations.py          # Data transformation functions
├── database-setup/                 # Database initialization scripts
│   ├── sourcedb.sql               # Source database schema
│   ├── destinationdb.sql          # Destination database schema
│   └── storedb.sql                # Store database schema
├── great_expectations/             # Great Expectations configuration
│   ├── checkpoints/               # Validation checkpoints
│   ├── expectations/              # Data expectation suites
│   └── great_expectations.yml     # Main GE configuration
├── filesystem/                     # Data storage directories
│   ├── raw/                       # Raw extracted data
│   └── stage/                     # Transformed staging data
├── source-data/                   # Sample input data
├── dest-data/                     # Output data directory
├── debugging/                     # Logging configuration
├── docker-compose.yml             # Multi-container setup
├── Dockerfile                     # Custom Airflow image
├── setup.sh                      # Automated setup script
└── requirements.txt               # Python dependencies
```

## 🛠️ Prerequisites

- Docker Desktop (recommended) or Docker Engine + Docker Compose
- Python 3.8+ (for local development)
- 8GB+ RAM (recommended for running all containers)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Anurag-Negi28/Airflow_GeX_Data_Pipeline.git
cd Airflow_GeX_Data_Pipeline
```

### 2. Automated Setup (Recommended)

Run the automated setup script that handles everything:

```bash
# On Linux/macOS
source setup.sh

# On Windows (Git Bash or WSL)
bash setup.sh
```

The setup script will:

- Create Python virtual environment
- Install dependencies
- Initialize Great Expectations
- Set up environment variables
- Start all Docker containers
- Configure Airflow connections
- Open the Airflow UI in your browser

### 3. Manual Setup (Alternative)

If you prefer manual setup:

#### Step 1: Environment Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r pip-chill-requirements.txt
```

#### Step 2: Configure Environment Variables

Create a `.env` file with the following variables:

```env
# Database Connections
SOURCEDB_CONN=postgresql+psycopg2://sourcedb1:sourcedb1@postgres-source:5432/sourcedb
DESTDB_CONN=postgresql+psycopg2://destdb1:destdb1@postgres-dest:5432/destdb
STOREDB_CONN=postgresql+psycopg2://storedb1:storedb1@postgres-store:5432/storedb

# Email Configuration
SMTP_ADDRESS=smtp.gmail.com
SMTP_PORT=587
SENDER_LOGIN=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECEIVER_EMAILS=recipient@example.com

# Airflow Configuration
AIRFLOW_UID=1000
AIRFLOW_GID=0
LOCAL_DIRECTORY=/path/to/your/project
```

#### Step 3: Start Services

```bash
# Create necessary directories
mkdir -p logs plugins

# Set permissions (Linux/macOS)
chmod 777 dags logs plugins filesystem database-setup source-data dest-data great_expectations

# Start containers
docker-compose up -d
```

#### Step 4: Configure Airflow Connections

```bash
# Run the connection setup script
bash airflow_conn.sh
```

## 🌐 Access Points

Once the setup is complete, you can access:

- **Airflow Web UI**: http://localhost:8080
  - Username: `airflow`
  - Password: `airflow`
- **PostgreSQL Databases**:
  - Source DB: `localhost:5433`
  - Destination DB: `localhost:5434`
  - Store DB: `localhost:5435`

## 📊 Pipeline Configuration

### Data Sources

The pipeline processes retail e-commerce data with the following schema:

```sql
CREATE TABLE ecommerce.retail_profiling (
  invoice_number VARCHAR(16),
  stock_code VARCHAR(32),
  detail VARCHAR(1024),
  quantity INT,
  invoice_date TIMESTAMP,
  unit_price NUMERIC(8, 3),
  customer_id INT,
  country VARCHAR(32)
);
```

### Great Expectations Suites

The project includes comprehensive data validation suites:

- **retail_source_suite**: Validates source data integrity
- **retail_load_suite**: Validates extracted raw data
- **retail_transform_suite**: Validates transformed data
- **retail_warehouse_suite**: Validates final warehouse data
- **retail_dest_suite**: Validates destination data completeness

### Data Transformations

Key transformations applied to the data:

1. **Data Cleaning**: Remove rows with null customer_id
2. **Country Standardization**: Replace "Unspecified" countries with null
3. **Type Conversion**: Convert customer_id to integer type
4. **Format Conversion**: Transform between CSV and Parquet formats

## 🔧 Customization

### Adding New Validation Rules

1. Create new expectation suites in `great_expectations/expectations/`
2. Define validation checkpoints in `great_expectations/checkpoints/`
3. Add validation tasks to the Airflow DAG

### Modifying Data Transformations

Edit the transformation functions in `dags/transformations.py`:

```python
def transform_raw_data(output_loc):
    # Add your custom transformations here
    df = pd.read_csv(f"{root_path}/filesystem/raw/retail_profiling-{date}.csv")
    # Your transformation logic
    df.to_parquet(output_loc)
```

### Adding New Data Sources

1. Create new SQL scripts in `dags/scripts/sql/`
2. Add corresponding Python scripts in `dags/scripts/python/`
3. Update the main DAG file to include new tasks

## 🐛 Troubleshooting

### Common Issues

1. **Container Permission Issues**

   ```bash
   sudo chmod 777 logs plugins filesystem
   ```

2. **Port Conflicts**

   - Check if ports 8080, 5433, 5434, 5435 are available
   - Modify `docker-compose.yml` to use different ports if needed

3. **Memory Issues**

   - Ensure Docker has at least 4GB RAM allocated
   - Consider using LocalExecutor instead of CeleryExecutor

4. **Connection Issues**
   - Verify database connections in Airflow UI
   - Run `bash airflow_conn.sh` to reset connections

### Logs and Debugging

- Airflow logs: `./logs/`
- Container logs: `docker-compose logs [service-name]`
- Setup logs: `./debugging/setup.log`
- Custom logging: `./debugging/logging.ini`

## 📝 Development

### Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run Great Expectations validation
great_expectations checkpoint run retail_source_checkpoint

# Test Airflow DAG
airflow dags test retail_data_pipeline
```

### Code Formatting

The project uses Black for code formatting:

```bash
black dags/ --line-length 88
```

## 🙏 Acknowledgments

- [Apache Airflow](https://airflow.apache.org/) for the workflow orchestration
- [Great Expectations](https://greatexpectations.io/) for data validation
- [PostgreSQL](https://www.postgresql.org/) for database management
- The open-source community for inspiration and tools

## Contributors

- **Anurag Negi**: Great Expectations Configuration, Architecture, Readme, Presentation  
- **Yash Pandey**: Apache Airflow Configuration, Documentation, Demo Video
