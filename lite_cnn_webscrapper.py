# Import necessary libraries
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import threading
import time
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Initialize variables to store headlines, links, and temperature for CNN, NPR, and Chicago
app.config['cnn_headlines'] = []
app.config['cnn_links'] = []
app.config['npr_headlines'] = []
app.config['npr_links'] = []
app.config['chicago_temperature'] = 'N/A'  # Default value

# Function to get headlines from CNN Lite and NPR
def get_cnn_lite_headlines():
    cnn_url = "https://lite.cnn.com"
    npr_url = "https://text.npr.org"

    # Get CNN headlines
    cnn_response = requests.get(cnn_url)
    cnn_soup = BeautifulSoup(cnn_response.content, "html.parser")

    cnn_headlines = []
    cnn_links = []

    for card_tag in cnn_soup.find_all("li", class_="card--lite"):
        headline_tag = card_tag.find("a")
        headline = headline_tag.text.strip()
        link = cnn_url + headline_tag["href"]
        cnn_headlines.append(headline)
        cnn_links.append(link)

    # Get NPR headlines
    npr_response = requests.get(npr_url)
    npr_soup = BeautifulSoup(npr_response.content, "html.parser")

    npr_headlines = []
    npr_links = []

    for li_tag in npr_soup.select('.topic-container li a.topic-title'):
        headline = li_tag.text.strip()
        link = npr_url + li_tag["href"]
        npr_headlines.append(headline)
        npr_links.append(link)

    return cnn_headlines, cnn_links, npr_headlines, npr_links

# Function to get the current temperature for Chicago using OpenWeatherMap API
def get_chicago_temperature():
    api_key = "98b5440c37229f24cae94a28398d3f03"  # Replace with your actual OpenWeatherMap API key

    # Make a request to the OpenWeatherMap API
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q=Chicago,us&units=imperial&appid={api_key}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        temperature = round(data.get('main', {}).get('temp', 'N/A'))
        return temperature
    else:
        return 'N/A'

# Function to refresh headlines and temperature in the background
def refresh_data():
    while True:
        cnn_headlines, cnn_links, npr_headlines, npr_links = get_cnn_lite_headlines()
        chicago_temperature = get_chicago_temperature()

        app.config['cnn_headlines'] = cnn_headlines
        app.config['cnn_links'] = cnn_links
        app.config['npr_headlines'] = npr_headlines
        app.config['npr_links'] = npr_links
        app.config['chicago_temperature'] = chicago_temperature
        app.config['last_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(900)  # Sleep for 15 minutes

# Start the thread to refresh headlines and temperature in the background
refresh_thread = threading.Thread(target=refresh_data)
refresh_thread.daemon = True
refresh_thread.start()

# Define a route for the main page
@app.route('/')
def index():
    # Retrieve headlines, links, temperature, and last update time from app configuration
    cnn_headlines = app.config.get('cnn_headlines', [])
    cnn_links = app.config.get('cnn_links', [])
    npr_headlines = app.config.get('npr_headlines', [])
    npr_links = app.config.get('npr_links', [])
    chicago_temperature = app.config.get('chicago_temperature', 'N/A')
    last_update = app.config.get('last_update', 'N/A')

    # Render the HTML template with the retrieved data
    return render_template('index.html', cnn_headlines=cnn_headlines, cnn_links=cnn_links,
                           npr_headlines=npr_headlines, npr_links=npr_links,
                           chicago_temperature=chicago_temperature, last_update=last_update)

# Run the Flask app if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='192.168.50.210', port=5000)
