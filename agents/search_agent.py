import requests

def fetch_papers(topic):
    url = f"https://api.crossref.org/works?query={topic}&rows=50"
    papers = []

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if status is not OK
        data = response.json()

        for item in data['message']['items']:
            if 'abstract' in item:  # Check if the paper has an abstract
                paper = {
                    "title": item['title'][0],
                    "year": item['published']['date-parts'][0][0],  # Extract year
                    "DOI": item['DOI'],
                    "abstract": item['abstract'],  # Abstract
                }
                papers.append(paper)
                if len(papers) >= 10:  # Limit to 5 papers
                    break

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching papers: {e}")
        return []  # Return an empty list in case of error
    
    return papers
