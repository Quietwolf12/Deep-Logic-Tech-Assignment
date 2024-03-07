from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import requests

url = 'https://time.com/'

app = FastAPI()

@app.get("/getTimeStories")
async def get_latest_stories():
  """
  Fetches and parses the latest stories from time.com and returns them as a JSON object array.
  """
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for unsuccessful responses

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the container for the latest stories 
    container = soup.find('div', {
        "data-module_name": "Latest Stories"
    })

    if container:
      # Extract information from each story item
      stories = []
      for item in container.find_all('li', class_="latest-stories__item"):
        link_element = item.find('a', href=True)
        title_element = item.find('h3', class_='latest-stories__item-headline')

        if all([link_element, title_element]):
          # absolute URL by prepending "https://time.com"
          absolute_link = f"https://time.com{link_element['href']}"
          story = {
            "title": title_element.text.strip(),
            "link": absolute_link
          }
          stories.append(story)
      return stories
    else:
      raise HTTPException(status_code=404, detail="Couldn't find the container for the latest stories.")
  except requests.exceptions.RequestException as e:
    raise HTTPException(status_code=500, detail=f"Error fetching stories: {e}")

# Run the API using `uvicorn main:app --host 0.0.0.0 --port {desired_port}`
