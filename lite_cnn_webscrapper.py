# Import necessary libraries
from flask import Flask, render_template, send_from_directory
import os
import requests
from bs4 import BeautifulSoup
import threading
import time
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Initialize variables to store headlines, links, and temperature for CNN, NPR, and Chicago
app.config.update(
    cnn_headlines=[],
    cnn_links=[],
    npr_headlines=[],
    npr_links=[],
    chicago_temperature='N/A',  # Default value
    last_update='N/A'
)

app.config['STATIC_FOLDER'] = 'static'

# Function to get headlines from a generic website
def get_headlines(url, tag, class_name, base_url='', text_inside_tag=False):
    """
    Extract headlines and links from a website.

    Parameters:
    - url: The URL of the website.
    - tag: The HTML tag containing the headlines.
    - class_name: The CSS class of the tag containing the headlines.
    - base_url: The base URL to be appended to relative links.
    - text_inside_tag: Boolean flag to indicate whether to get the text inside the tag even if split across multiple nodes.

    Returns:
    - headlines: List of extracted headlines.
    - links: List of corresponding links.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    headlines = []
    links = []

    for card_tag in soup.find_all(tag, class_=class_name):
        headline_tag = card_tag.find("a")

        if headline_tag is not None:
            # Get the text inside the anchor tag
            if text_inside_tag:
                headline = headline_tag.get_text(separator=' ', strip=True)

            else:
                headline = headline_tag.text.strip()

            link = base_url + headline_tag["href"]
            headlines.append(headline)
            links.append(link)
        else:
            print("No headline tag found:", card_tag)

    return headlines, links

# Function to get headlines from CNN Lite
def get_cnn_lite_headlines():
    cnn_url = "https://lite.cnn.com"
    return get_headlines(cnn_url, "li", "card--lite", cnn_url)

# Function to get headlines from NPR
def get_npr_headlines():
    npr_url = "https://text.npr.org"
    response = requests.get(npr_url)
    soup = BeautifulSoup(response.content, "html.parser")

    headlines = []
    links = []

    for li_tag in soup.select('.topic-container li'):
        headline_tag = li_tag.find("a", class_="topic-title")

        if headline_tag is not None:
            headline = ' '.join([text.strip() for text in headline_tag.find_all(text=True)])
            link = npr_url + headline_tag["href"]
            headlines.append(headline)
            links.append(link)
        else:
            print("No headline tag found:", li_tag)

    return headlines, links

# Function to get the current temperature for Chicago using OpenWeatherMap API
def get_chicago_temperature(api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q=Chicago,us&units=imperial&appid={api_key}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        temperature = round(data.get('main', {}).get('temp', 'N/A'))
        return temperature
    else:
        return 'N/A'

# Function to refresh headlines and temperature
def refresh_data():
    while True:
        # Get headlines from CNN Lite
        cnn_headlines, cnn_links = get_cnn_lite_headlines()

        # Get headlines from NPR
        npr_headlines, npr_links = get_npr_headlines()

        # Get the current temperature for Chicago
        chicago_temperature = get_chicago_temperature(api_key="place_holder")

        # Update the app configuration with the latest data
        app.config.update(
            cnn_headlines=cnn_headlines,
            cnn_links=cnn_links,
            npr_headlines=npr_headlines,
            npr_links=npr_links,
            chicago_temperature=chicago_temperature,
            last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        # Sleep for 15 minutes before refreshing again
        time.sleep(900)

# Run the refresh_data function before the first request is processed
@app.before_first_request
def activate_job():
    refresh_thread = threading.Thread(target=refresh_data)
    refresh_thread.start()

# Define a route for the main page
@app.route('/')
def index():
    # Retrieve headlines, links, temperature, and last update time from app configuration
    data = app.config
    return render_template('index.html', **data)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, app.config['STATIC_FOLDER']),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

# Run the Flask app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='192.168.50.210', port=5000)
