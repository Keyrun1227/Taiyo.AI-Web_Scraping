# 📑 Methodologies

Welcome to the Methodologies document! Here, we provide detailed explanations of the scripts and methodologies used in the Data Engineering Trial Task project.

## 1. DataExtractionAndStandardization.py

### 🎯 Purpose:
This script combines the tasks of data extraction and standardization. It fetches HTML content from a list of input URLs, extracts relevant information, and standardizes the data according to provided data standards.

### 🚀 Usage:
1. Input URLs are read from the `input_urls.csv` file in the `data` folder.
2. HTML content is fetched using the `fetch_html_content` function.
3. Information is extracted using the `extract_information` function.
4. Data is standardized using the `standardize_data` function.
5. Standardized data is written to the `standardized_data.csv` file in the `data` folder.

## 2. ResearchAndDataSourcing.py

### 🎯 Purpose:
This script focuses on the initial phase of data sourcing and research. It fetches HTML content from a list of input URLs and generates summaries using BERT-based summarization.

### 🚀 Usage:
1. Input URLs are read from the `input_urls.csv` file in the `data` folder.
2. HTML content is fetched using the `fetch_content` function.
3. Summaries are generated using the `generate_summary` function.
4. Relevant links are selected based on scores calculated from the summaries.
5. Top relevant links are printed for further processing.

## 3. Combined_Tasks_Code.py

### 🎯 Purpose:
This script combines various tasks, including research, data extraction, and standardization, into a single script. It provides a comprehensive approach to data processing from initial research to standardized output.

### 🚀 Usage:
1. Input URLs are read from the `input_urls.csv` file in the `data` folder.
2. Research and data sourcing are performed to select relevant links.
3. HTML content is fetched using the `fetch_html_content` function.
4. Information is extracted using the `extract_information` function.
5. Data is standardized using the `standardize_data` function.
6. Standardized data is written to the `standardized_data.csv` file in the `data` folder.

## 4. AutomatedDataProcessing.py

### 🎯 Purpose:
This script demonstrates continuous data updating by implementing an automated process. It runs in an infinite loop, periodically fetching the latest data from input URLs, and updating the standardized data accordingly.

### 🚀 Usage:
1. Input URLs are read from the `input_urls.csv` file in the `data` folder.
2. The main function runs in an infinite loop with a delay for continuous updating.
3. Data scraping and standardization process is executed at regular intervals.
4. Standardized data is continuously updated in the `standardized_data.csv` file in the `data` folder.

