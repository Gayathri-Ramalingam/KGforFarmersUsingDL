import wikipediaapi
import requests
from bs4 import BeautifulSoup
import time

# Wikipedia data retrieval with user-agent
def get_wikipedia_data(topic):
    user_agent = "MyWikipediaBot/1.0 (boops085@gmail.com)"  # Specify your user agent
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent=user_agent  # Use a proper user-agent
    )
    
    page = wiki_wiki.page(topic)

    if not page.exists():
        print(f"{topic} not found on Wikipedia.")
        return ""
    
    return page.text

# Fetch data from web sources
def get_web_data(search_term, num_sources=5):
    headers = {'User-Agent': 'Mozilla/5.0'}
    search_url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}&num={num_sources}"
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for g in soup.find_all('a', href=True):
        href = g['href']
        if 'url?q=' in href and 'webcache' not in href:
            link = href.split('url?q=')[1].split('&')[0]
            if len(links) < num_sources:
                links.append(link)

    data = ""
    for link in links:
        try:
            res = requests.get(link, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            paragraphs = soup.find_all('p')
            text = "\n".join([p.text for p in paragraphs[:5]])  # Fetch first 5 paragraphs
            data += f"\n\nSource: {link}\n{text}\n"
            
            time.sleep(2)  # To avoid being blocked by rapid requests
        except Exception as e:
            print(f"Failed to retrieve data from {link}: {e}")
    
    return data

# Main script execution
def main():
    topic = "Agriculture"
    search_term = "Agriculture latest information"
    
    print("Fetching Wikipedia data...")
    wikipedia_content = get_wikipedia_data(topic)
    
    print("Fetching web source data...")
    web_content = get_web_data(search_term)
    
    combined_content = f"WIKIPEDIA DATA:\n\n{wikipedia_content}\n\nWEB SOURCES:\n\n{web_content}"
    
    # Save the combined data into a text file
    with open("agriculture_info.txt", "w", encoding="utf-8") as file:
        file.write(combined_content)
    
    print("Data saved to agriculture_info.txt")

# Run the script
if __name__ == "__main__":
    main()
