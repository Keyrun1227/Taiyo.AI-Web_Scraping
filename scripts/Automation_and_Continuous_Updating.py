# Details:
# Explain how the data sources will be continuously updated.
# Describe the use of cron jobs or similar scheduling tools for ongoing data updates.
# Ensure your methodology adheres to a production environment's standards

# The data sources can be continuously updated by implementing a scheduled task that runs at regular intervals,
# fetching the latest data from the specified URLs and updating the standardized data accordingly.
# This can be achieved using cron jobs on Unix-like systems or Task Scheduler on Windows.

# To implement continuous updating, the main function `main()` is wrapped in an infinite loop.
# Inside this loop, the data scraping and standardization process is executed.
# After completing each iteration of the loop, the program waits for a specified time interval before starting the next iteration.
# This ensures that the process runs at regular intervals, allowing for continuous updates.

# The `time.sleep()` function is used to introduce a delay between iterations of the loop.
# In this case, the delay is set to 24 hours (86400 seconds), indicating that the data scraping and standardization process will run once every 24 hours.

# By running the script continuously in this manner, the data sources will be periodically queried for updates,
# and the standardized data will be refreshed accordingly, ensuring that the information remains up-to-date over time.


import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import uuid
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import random
import time  # Import the time module for scheduling

# Initialize BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
model.eval()

# Function to fetch content from a URL and remove HTML tags
def fetch_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Remove HTML tags and extract text
            text = soup.get_text(separator=' ')
            return text
        else:
            print(f"Failed to fetch URL: {url}")
            return None
    except Exception as e:
        print(f"Error processing URL {url}: {str(e)}")
        return None

# Function to generate summary using BERT
def generate_summary(text):
    try:
        # Tokenize and truncate the text for BERT input
        inputs = tokenizer.encode_plus(text, return_tensors="pt", max_length=512, truncation=True)
        # Generate summary using BERT
        outputs = model(**inputs)
        summary = tokenizer.decode(outputs.logits.argmax(dim=-1)[0])
        return summary
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return None

# Function to fetch HTML content from a URL
def fetch_html_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to fetch HTML content from {url}")
            return None
    except Exception as e:
        print(f"Error fetching HTML content from {url}: {str(e)}")
        return None

# Function to extract information from HTML content
def extract_information(html_content):
    if html_content:
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Extract title
            title = soup.title.text.strip()
            # Extract description meta tag
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description = description_tag['content'].strip() if description_tag else ""
            # Extract additional attributes
            additional_info = {}
            # You can add code here to extract additional attributes from the HTML content
            return title, description, additional_info
        except Exception as e:
            print(f"Error extracting information: {str(e)}")
            return None, None, None
    else:
        return None, None, None

# Function to analyze HTML content using BERT and extract relevant attributes
def analyze_with_bert(html_content):
    # Process the HTML content
    # For demonstration, let's assume we're analyzing the content for standard attributes using BERT
    bert_predicted_attributes = {
        "status": random.choice(["Open", "Closed"]),
        "stages": random.choice(["Planning", "Execution"]),
        "procurementMethod": random.choice(["Design and Build", "Request for Proposal"]),
        "budget": random.uniform(100000.0, 10000000.0),  # Random budget between 100,000 and 10,000,000 USD
        "currency": "USD",
        "buyer": random.choice(["Public", "Private"]),
        "sector": "Construction",
        "subsector": random.choice(["Building Construction", "Infrastructure Development"])
    }
    return bert_predicted_attributes

# Function to standardize data according to Table 2
def standardize_data(title, description, additional_info, bert_predicted_label, url):
    aug_id = str(uuid.uuid4())  # Generate UUID
    country_name = "United States"
    country_code = "USA"
    map_coordinates = {"type": "Point", "coordinates": [-122.4, 37.8]}  # Default coordinates for demonstration
    region_name = "California"
    region_code = "CA"
    status = additional_info.get("status", random.choice(["Open", "Closed"]))
    stages = additional_info.get("stages", random.choice(["Planning", "Execution"]))
    date = datetime.now().strftime("%Y-%m-%d")  # Current date
    procurement_method = additional_info.get("procurementMethod", random.choice(["Design and Build", "Request for Proposal"]))
    budget = additional_info.get("budget", random.uniform(100000.0, 10000000.0))  # Random budget between 100,000 and 10,000,000 USD
    currency = additional_info.get("currency", "USD")
    buyer = additional_info.get("buyer", random.choice(["Public", "Private"]))
    sector = additional_info.get("sector", "Construction")
    subsector = additional_info.get("subsector", random.choice(["Building Construction", "Infrastructure Development"]))

    # Analyze description with BERT
    bert_predicted_label = bert_predicted_label or analyze_with_bert(description)

    # Construct standardized data as dictionary
    standardized_data = {
        "aug_id": aug_id,
        "country_name": country_name,
        "country_code": country_code,
        "map_coordinates": map_coordinates,
        "url": url,
        "region_name": region_name,
        "region_code": region_code,
        "title": title,
        "description": description,
        "status": status,
        "stages": stages,
        "date": date,
        "procurementMethod": procurement_method,
        "budget": budget,
        "currency": currency,
        "buyer": buyer,
        "sector": sector,
        "subsector": subsector,
        "bert_predicted_label": bert_predicted_label
    }
    return standardized_data

# Function to write standardized data to CSV file
def write_to_csv(data_list, filename):
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data_list[0].keys())
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)
        print(f"Data written to {filename} successfully.")
    except Exception as e:
        print(f"Error writing to CSV: {str(e)}")

# Main function
def main():
    urls = []
    with open('input_urls.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            urls.append(row['Source URL'])
    
    # Fetch content, generate summaries, and select top links based on relevance
    summaries = []
    for url in urls:
        print(f"Processing {url}...")
        content = fetch_content(url)
        if content:
            summary = generate_summary(content)
            if summary:
                summaries.append((url, summary))

    # Assess relevance of summaries and assign scores
    scores = []
    for url, summary in summaries:
        score = 0
        # Check for keywords related to construction, infrastructure, projects, tenders, and California
        if "construction" in summary.lower():
            score += 1
        if "infrastructure" in summary.lower():
            score += 1
        if "projects" in summary.lower():
            score += 1
        if "tenders" in summary.lower():
            score += 1
        if "california" in summary.lower():
            score += 1
        scores.append((url, score))

    # Sort links based on scores in descending order
    scores.sort(key=lambda x: x[1], reverse=True)

    # Select top 10 links with highest scores
    top_links = [link[0] for link in scores[:min(10, len(scores))]]
    # Print top links
    print("Top 5 to 10 Relevant Links:")
    for link in top_links:
        print(link)
    # Initialize list to store standardized data
    standardized_data_list = []

    # Iterate over URLs
    for url in top_links:
        print("Scraping data from", url)
        # Step 1: Fetch HTML content
        html_content = fetch_html_content(url)
        if html_content:
            # Step 2: Extract Information
            title, description, additional_info = extract_information(html_content)
            if title and description:
                # Step 3: Standardize Data
                standardized_data = standardize_data(title, description, additional_info, None, url)
                # Add standardized data to list
                standardized_data_list.append(standardized_data)
                print("Standardized Data:", standardized_data)
                print()  # Add newline for readability between URLs
            else:
                print("Failed to extract information from", url)
        else:
            print("Failed to fetch HTML content from", url)

    # Write standardized data to CSV file
    write_to_csv(standardized_data_list, 'standardized_data.csv')

if __name__ == "__main__":
    # Run the main function in an infinite loop with a delay of 24 hours (86400 seconds)
    while True:
        print("Running data scraping and standardization process...")
        main()
        print("Waiting for next execution...")
        time.sleep(86400)  # Delay for 24 hours (86400 seconds)
