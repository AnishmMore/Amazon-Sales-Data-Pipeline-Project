This repository contains an end-to-end data engineering pipeline designed to process and analyze Amazon's mobile phone sales data. The data encompasses a year's worth of sales from three regions: India, USA, and France. The pipeline employs modern data engineering practices and tools to handle data ingestion, transformation, and visualization effectively.

# Project Overview
The Amazon Sales Data Pipeline Project is an integration of various data engineering components that work together to transform raw sales data into insightful analytical reports. The pipeline processes data in multiple formats, including CSV, JSON, and Parquet, using Apache Airflow for orchestration and Snowflake for storage and computation. The final output is a dashboard that visualizes key metrics and trends in the data.

# Architecture
The architecture is split into several zones, each responsible for different aspects of the data lifecycle:

1. Data Pipeline Architecture
![Data Pipeline Architecture](https://github.com/AnishmMore/Amazon-Sales-Data-Pipeline-Project/blob/main/data_pipeline.jpg)

2. Airflow DAGs
![Airflow DAGs](https://github.com/AnishmMore/Amazon-Sales-Data-Pipeline-Project/blob/main/DAG_graph.png)

# Pipeline Stages:
Ingestion: Data files are ingested into Snowflake's internal staging area.
Source Zone: Initial storage where data is categorized by item, customer, and sales.
Curated Zone: Data is cleaned and transformed using Snowpark's DataFrame API.
Consumption Zone: Data is modeled dimensionally to facilitate easy and efficient querying.

# Tools and Technologies
- **Apache Airflow:** Orchestrating and scheduling data pipeline tasks.
- **Snowflake:** Storing and processing data in internal staging, source, curated, and consumption zones.
- **Snowpark:** Data transformation and computation in Snowflake.
- **Dashboard Tool:** Visualizing data (mention the specific tool you used).

# Data Flow Exploration
The project illustrates an efficient ETL data flow, showcasing Snowpark in tandem with Snowflake. Key highlights include:

- **Data Loading:** Streamlining the ingestion from local files to Snowflake's internal stage.
- **Data Curation:** Employing Snowpark's DataFrame API to ensure data quality through transformations and cleaning.
- **Dimensional Modelling:** Implementing a dimensional model to structure the data, enhancing its analytical utility.

# Setup and Execution
To set up and run this pipeline, follow these steps:

## Configure Apache Airflow:

- Ensure Apache Airflow is installed and properly configured with the necessary dependencies.
- Configure the Airflow environment to connect to your Snowflake instance by setting up the appropriate Airflow connections.

## Set up Snowflake:

- Create a Snowflake account if you don't already have one.
- Within Snowflake, set up the required databases, warehouses, and any relevant schemas following the best practices for security and performance.

## Airflow DAG:

- Place the DAG file that defines the entire pipeline in the dags/ directory of your Airflow installation.
- Make sure to update the Airflow scheduler to pick up the new DAG.

## Data Transformation with Snowpark:

- Utilize the Snowpark scripts located in the snowpark/ directory to perform data transformation and computation tasks.
- Ensure that the Snowpark scripts are configured to connect to your Snowflake instance with the correct credentials.

## Visualization Dashboard:

- Once the data has been processed and loaded into the final tables in Snowflake, access the dashboard through the specified visualization tool to see the results.
- Make sure to document how to configure the dashboard tool to connect to Snowflake and retrieve the data for visualization.

## Execution:

- Trigger the Airflow DAG manually through the Airflow UI or set it to run on a schedule.
- Monitor the DAG's execution status via the Airflow UI to ensure that each task is completed successfully.
- Remember to replace any placeholders with your actual file paths, script names, and other specifics related to your project setup.

# Output:
The dashboard highlights key metrics and trends, offering insights into various aspects of Amazon's mobile phone sales data. The visualizations are designed to facilitate easy understanding of the data, enabling stakeholders to make informed decisions.

## Dashboard Features:

- Yearly Data Overview: A visualization of the entire year's data, providing a snapshot of sales performance over time.
- Country-wise Payment Analysis: Detailed charts and graphs depict payment methods and preferences across different countries, namely India, USA, and France.
- Sales Metrics: Interactive elements that allow users to explore sales figures, customer demographics, and item categories.
![Dashboard](https://github.com/AnishmMore/Amazon-Sales-Data-Pipeline-Project/blob/main/dashboards/Screenshot%202023-11-06%20at%204.44.48%E2%80%AFPM.png)

# Contact
For any queries or further discussion regarding this project, feel free to contact Anish More.
