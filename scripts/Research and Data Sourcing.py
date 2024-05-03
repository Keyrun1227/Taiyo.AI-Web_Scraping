import requests
from bs4 import BeautifulSoup
from transformers import BertTokenizer, BertForSequenceClassification

# Define the BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# URLs of the suggested data sources
urls = [
    "https://www.ci.richmond.ca.us/1404/Major-Projects",
    "https://www.bakersfieldcity.us/518/Projects-Programs",
    "https://www.cityofwasco.org/311/Current-Projects",
    "https://www.eurekaca.gov/744/Upcoming-Projects",
    "https://www.cityofarcata.org/413/Current-City-Construction-Projects",
    "https://www.mckinleyvillecsd.com/news-and-project-updates",
    "https://www.cityofsanrafael.org/major-planning-projects-2/",
    "https://www.novato.org/government/community-development/planning-division/planning-projects?locale=en",
    "https://www.cityofmillvalley.org/258/Projects",
    "https://riversideca.gov/utilities/projects",
    "https://www.moval.org/cdd/documents/about-projects.html",
    "https://www.coronaca.gov/government/departments-divisions/department-of-water-and-power/construction",
    "http://www.cityofsacramento.org/public-works/engineering-services/projects",
    "https://www.citrusheights.net/292/Current-Projects",
    "https://www.elkgrovecity.org/southeast-policy-area/development-projects",
    "https://www.sbcity.org/city_hall/community_economic_development/development_projects",
    "https://www.fontanaca.gov/765/Current-Projects",
    "https://www.ontarioca.gov/Planning/CurrentPlanning",
    "https://www.chulavistaca.gov/departments/development-services/city-projects",
    "https://www.ci.oceanside.ca.us/government/development-services/engineering/capital-improvement-program/current-projects",
    "https://www.slocity.org/government/department-directory/parks-and-recreation/current-projects",
    "https://www.prcity.com/363/City-Projects",
    "https://www.atascadero.org/index.php?option=com_content&view=article&id=652&Itemid=1723",
    "https://www.cityofsanmateo.org/1176/Whats-Happening-in-Development",
    "https://www.dalycity.org/362/Current-Project-List",
    "https://www.cityoflompoc.com/government/departments/economic-community-development/planning-division/major-project-updates",
    "https://www.santamariagroup.com/projects",
    "https://www.santaclaraca.gov/business-development/development-projects/projects-listing",
    "https://www.ci.vacaville.ca.us/government/community-development/major-development-projects?locale=en",
    "https://www.cityofvallejo.net/our_city/departments_divisions/planning_development_services/economic_development_department/development_projects",
    "https://www.fairfield.ca.gov/government/city-departments/community-development/planning-division/development-activity?locale=en",
    "https://www.fairfield.ca.gov/government/city-departments/public-works/capital-improvement-projects",
    "https://www.rpcity.org/city_hall/departments/development_services/engineering/projects_in_progress",
    "https://www.srcity.org/3212/Current-Projects",
    "https://cityofpetaluma.org/planning-projects/",
    "https://www.toaks.org/departments/public-works/construction",
    "https://www.simivalley.org/departments/public-works/public-works-engineering/capital-projects/current-capital-projects",
    "https://www.shorelinewa.gov/government/projects-initiatives"
]

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
