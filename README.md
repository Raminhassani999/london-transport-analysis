# London Transport Analysis | Data Engineering Project

An end-to-end Data Engineering project focused on processing, validating, storing, and analyzing Transport for London (TfL) journey data using Python, Pandas, Snowflake, and SQL.

The project demonstrates a practical ETL workflow, from raw CSV ingestion to cloud-based data warehousing and analytical transformations.

## Project Overview

This project analyzes public transport usage in London across different transportation modes, including buses, Underground, DLR, trams, Overground, London Cable Car, and TfL Rail.

The dataset contains 213 reporting periods spanning April 2010 to August 2026.

The main objectives are to:

- Build a reproducible data cleaning and validation pipeline.
- Prepare raw transport data for analytical processing.
- Load structured data into a Snowflake data warehouse.
- Implement reusable SQL transformations.
- Analyze transport usage trends and year-over-year changes.
- Explore modern data transformation workflows using dbt.

## Tech Stack

- **Python:** Data processing and ETL development
- **Pandas:** Data cleaning, transformation, and validation
- **Snowflake:** Cloud data warehouse
- **SQL:** Data validation and analytical transformations
- **dbt Core:** SQL transformation project setup
- **uv:** Python dependency and environment management
- **Git & GitHub:** Version control and project documentation

## Pipeline Architecture

```text
Transport for London Dataset
             |
             v
       Raw CSV File
             |
             v
       Python + Pandas
       - Data Cleaning
       - Date Conversion
       - Data Validation
       - Column Standardization
             |
             v
       Processed CSV File
             |
             v
       Snowflake Warehouse
             |
       RAW.JOURNEYS_RAW
             |
             v
       SQL Transformations
             |
             v
       ANALYTICS Schema
       - JOURNEYS_YEARLY
       - JOURNEYS_YEARLY_GROWTH
             |
             v
       Transport Analysis
```

## Data Processing

### 1. Data Extraction

The original TfL journey dataset is loaded from a CSV file using Pandas.

The dataset contains journey counts, expressed in millions, for multiple public transportation modes.

### 2. Data Cleaning and Transformation

The Python cleaning pipeline performs:

- Column-name standardization using snake_case.
- Date conversion into consistent datetime formats.
- Missing-value analysis.
- Duplicate-record detection.
- Financial-year label validation and correction.
- Reporting-period date validation.
- Calculation of reporting-period durations.

Missing journey values are preserved rather than automatically replaced with zero.

### 3. Data Validation

The cleaning process checks data consistency before loading it into Snowflake.

Validation includes:

- Verifying chronological order.
- Detecting invalid date ranges.
- Checking financial-year labels.
- Identifying duplicate reporting periods.
- Comparing reported period durations with calculated calendar days.

Six discrepancies between reported and calculated period durations were identified. The original values were preserved, and a separate `calculated_days` column was added for comparison.

### 4. Data Loading

The cleaned dataset is exported to:

`data/processed/tfl_journeys_clean.csv`

It is then loaded into Snowflake.

**Destination table:**

`LONDON_TRANSPORT.RAW.JOURNEYS_RAW`

The loaded dataset contains 213 rows and 13 columns.

## Snowflake Data Warehouse

The Snowflake database is organized into two schemas.

### RAW Schema

Contains the ingested, cleaned transport dataset.

**Table:** `JOURNEYS_RAW`

### ANALYTICS Schema

Contains reusable analytical SQL views.

**View 1: `JOURNEYS_YEARLY`**

Aggregates recorded transport journeys by reporting-period start year.

**View 2: `JOURNEYS_YEARLY_GROWTH`**

Calculates year-over-year changes in bus and Underground journey volumes using SQL window functions.

These views provide reusable transformations for reporting and further analysis.

## Data Analysis

The project explores:

- Total recorded journeys by transport mode.
- Historical changes in Underground usage.
- Year-over-year journey growth.
- Transport usage during the COVID-19 period.
- Post-pandemic recovery patterns.

The analysis identified a substantial decline in Underground usage during 2020, followed by a gradual recovery in subsequent years.

Yearly results are grouped by the start date of each reporting period. Consequently, they are not exact calendar-year allocations, and partial-year coverage must be considered when interpreting comparisons.

## dbt Integration

dbt Core and the Snowflake adapter have been installed to support the next stage of the project.

The planned integration will move existing SQL transformations into version-controlled dbt models and introduce automated data-quality tests.

## Running the Python Pipeline

Install project dependencies:

```bash
uv sync
```

Execute the cleaning pipeline:

```bash
uv run python clean_data.py
```

The cleaned dataset is generated at:

```text
data/processed/tfl_journeys_clean.csv
```

## Project Structure

```text
london-transport-analysis/
│
├── data/
│   ├── raw/
│   │   └── tfl-journeys-type.csv
│   └── processed/
│       └── tfl_journeys_clean.csv
│
├── src/
│   └── london_transport_analysis/
│
├── clean_data.py
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md
```

## Future Improvements

- Complete dbt integration with Snowflake.
- Add automated data-quality tests.
- Automate CSV ingestion and warehouse loading.
- Introduce workflow orchestration.
- Implement incremental data processing.
- Build interactive dashboards for transport analysis.
- Add monitoring and pipeline reliability checks.

## Key Learning Outcomes

This project provides practical experience in:

- Developing ETL pipelines with Python and Pandas.
- Cleaning and validating real-world datasets.
- Working with cloud data warehouses.
- Designing RAW and ANALYTICS data layers.
- Creating reusable SQL views.
- Applying SQL window functions for trend analysis.
- Preparing analytical transformations for dbt.
- Managing a Data Engineering project with Git and GitHub.

## Project Purpose

Developed as a hands-on portfolio project to strengthen practical Data Engineering skills and gain experience with data processing, cloud data warehousing, SQL transformations, and modern analytics engineering workflows.
