import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_quotes():
    # 1. Define the target URL
    url = "http://quotes.toscrape.com/"
    
    # 2. Send an HTTP GET request to the website
    # Adding a standard User-Agent header helps avoid getting blocked by some sites
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print(f"Fetching data from {url}...")
    response = requests.get(url, headers=headers)
    
    # 3. Check if the request was successful (Status Code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the web page. Status Code: {response.status_code}")
        return

    # 4. Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 5. Identify and extract the relevant data
    # On this specific site, each quote is wrapped in a <div> with the class "quote"
    quotes_data = []
    quote_elements = soup.find_all("div", class_="quote")
    
    for element in quote_elements:
        # Extract the text of the quote
        text = element.find("span", class_="text").text.strip()
        
        # Extract the author
        author = element.find("small", class_="author").text.strip()
        
        # Append to our list as a dictionary
        quotes_data.append({
            "Quote": text,
            "Author": author
        })
        
    # 6. Be polite to the server (Rate Limiting)
    time.sleep(1) 
    
    # 7. Convert the extracted data into a Pandas DataFrame for analysis
    df = pd.DataFrame(quotes_data)
    
    # 8. Display the first few rows and export to CSV
    print("\nScraping successful! Here is a preview of your dataset:\n")
    print(df.head())
    
    # Save the dataset to your computer
    df.to_csv("scraped_quotes.csv", index=False, encoding="utf-8")
    print("\nData has been saved to 'scraped_quotes.csv'.")

# Run the function
if __name__ == "__main__":
    scrape_quotes()