import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import uuid
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Initialize BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
model.eval()

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
        "status": "Open",
        "stages": "Planning",
        "procurementMethod": "Unknown",
        "budget": 0.0,
        "currency": "USD",
        "buyer": "Unknown",
        "sector": "Unknown",
        "subsector": "Unknown"
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
    status = additional_info.get("status", "Open")
    stages = additional_info.get("stages", "Planning")
    date = datetime.now().strftime("%Y-%m-%d")  # Current date
    procurement_method = additional_info.get("procurementMethod", "Unknown")
    budget = additional_info.get("budget", 0.0)
    currency = additional_info.get("currency", "USD")
    buyer = additional_info.get("buyer", "Unknown")
    sector = additional_info.get("sector", "Unknown")
    subsector = additional_info.get("subsector", "Unknown")

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

# Main function
def main():
    # List of URLs to scrape
    urls = [
        "https://www.ci.richmond.ca.us/1404/Major-Projects",
        "https://www.bakersfieldcity.us/518/Projects-Programs",
        "https://www.cityofwasco.org/311/Current-Projects",
        "https://www.eurekaca.gov/744/Upcoming-Projects",
        "https://www.cityofarcata.org/413/Current-City-Construction-Projects",
        "https://www.mckinleyvillecsd.com/news-and-project-updates",
        "https://www.cityofsanrafael.org/major-planning-projects-2/",
        "https://www.cityofmillvalley.org/258/Projects",
        "https://riversideca.gov/utilities/projects",
        "https://www.moval.org/cdd/documents/about-projects.html"
    ]


    # Iterate over URLs
    for url in urls:
        print("Scraping data from", url)
        # Step 1: Fetch HTML content
        html_content = fetch_html_content(url)
        if html_content:
            # Step 2: Extract Information
            title, description, additional_info = extract_information(html_content)
            if title and description:
                # Step 3: Standardize Data
                standardized_data = standardize_data(title, description, additional_info, None, url)
                # Print or store standardized data as needed
                print("Standardized Data:", standardized_data)
                print()  # Add newline for readability between URLs
            else:
                print("Failed to extract information from", url)
        else:
            print("Failed to fetch HTML content from", url)

if __name__ == "__main__":
    main()