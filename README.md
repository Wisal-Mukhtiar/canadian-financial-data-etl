
# USD to CAD expense conversion ETL pipeline

### Overview
This project is an ETL (extract, transform, load) pipeline for extracting data from the Bank of Canada's Valet API, performing necessary transformations, and loading the data into a MySQL database. It uses the petl Python module for processing the data.


## Pipeline Steps
The pipeline consists of the following steps:

1. Extract the USD to Canadian Dollar exchange rate    data from the Bank of Canada Valet API for a given start date.
2. Read an expenses xlsx file which contains expenses in USD with their corresponding dates.
3. Process the exchange rate data by removing any unnecessary columns and rows, and store it as a petl table with columns 'date' and 'rate'.
4. Read the expenses data as a petl table.
5. Join the two tables on their common 'date' column, and fill in any missing values in the 'rate' column using the previous non-null value.
6. Drop rows with no expenses and add a new 'CAD' column to the table, which contains the expenses in Canadian dollars (converted from USD using the corresponding exchange rate).
7. Load the final table into a MySQL database.

## Installation
To run the pipeline, you need to have Python 3 and the following Python packages installed:

* petl
* requests
* pymssql
* configparser
* json
* datetime

The requirements need to be installed via pip are included in the requirements.txt file.

## Configuration
Before running the pipeline, you need to set the configuration parameters in the 'project.ini' file. The following parameters need to be set:

* startDate: the start date for extracting the exchange rate data from the Bank of Canada Valet API. This should be in the format 'YYYY-MM-DD'.
* url: the URL of the Bank of Canada Valet API.
* server: the name of the MySQL server where the data will be loaded.
* database: the name of the MySQL database where the data will be loaded.

## Usage
To run the pipeline, simply execute the main.py script:

# Bank of Canada ETL Pipeline

### Overview
This project is an ETL (extract, transform, load) pipeline for extracting data from the Bank of Canada's Valet API, performing necessary transformations, and loading the data into a MySQL database. It uses the petl Python module for processing the data.


## Pipeline Steps
The pipeline consists of the following steps:

1. Extract the USD to Canadian Dollar exchange rate    data from the Bank of Canada Valet API for a given start date.
2. Read an expenses xlsx file which contains expenses in USD with their corresponding dates.
3. Process the exchange rate data by removing any unnecessary columns and rows, and store it as a petl table with columns 'date' and 'rate'.
4. Read the expenses data as a petl table.
5. Join the two tables on their common 'date' column, and fill in any missing values in the 'rate' column using the previous non-null value.
6. Drop rows with no expenses and add a new 'CAD' column to the table, which contains the expenses in Canadian dollars (converted from USD using the corresponding exchange rate).
7. Load the final table into a MySQL database.

## Installation
To run the pipeline, you need to have Python 3 and the following Python packages installed:

* petl
* requests
* pymssql
* configparser
* json
* datetime

The requirements need to be installed via pip are included in the requirements.txt file.

## Configuration
Before running the pipeline, you need to set the configuration parameters in the 'project.ini' file. The following parameters need to be set:

* startDate: the start date for extracting the exchange rate data from the Bank of Canada Valet API. This should be in the format 'YYYY-MM-DD'.
* url: the URL of the Bank of Canada Valet API.
* server: the name of the MySQL server where the data will be loaded.
* database: the name of the MySQL database where the data will be loaded.

## Usage
```bash
  python main.py

```
This will read the configuration parameters from the 'project.ini' file, extract the exchange rate and expenses data, process it, and load it into the MySQL database. The script will print status updates and error messages to the console.
