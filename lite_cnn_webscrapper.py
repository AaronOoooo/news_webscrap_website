from flask import Flask, render_template, send_from_directory
import os
import requests
from bs4 import BeautifulSoup
import threading
import time
from datetime import datetime
from flask_cors import CORS
from dotenv import load_dotenv  # Import dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)

app.config.update(
    cnn_headlines=[],
    cnn_links=[],
    npr_headlines=[],
    npr_links=[],
    chicago_temperature='N/A',
    last_update='N/A'
)

app.config['STATIC_FOLDER'] = 'static'

data_initialized = False

def get_headlines(url, tag, class_name, base_url='', text_inside_tag=False):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    headlines = []
    links = []

    for card_tag in soup.find_all(tag, class_=class_name):
        headline_tag = card_tag.find("a")

        if headline_tag is not None:
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

def get_cnn_lite_headlines():
    cnn_url = "https://lite.cnn.com"
    return get_headlines(cnn_url, "li", "card--lite", cnn_url)

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

def get_chicago_temperature(api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q=Chicago,us&units=imperial&appid={api_key}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        temperature = round(data.get('main', {}).get('temp', 'N/A'))
        return temperature
    else:
        return 'N/A'

def refresh_data():
    while True:
        cnn_headlines, cnn_links = get_cnn_lite_headlines()
        npr_headlines, npr_links = get_npr_headlines()
        chicago_temperature = get_chicago_temperature(api_key=os.getenv("API_KEY"))

        app.config.update(
            cnn_headlines=cnn_headlines,
            cnn_links=cnn_links,
            npr_headlines=npr_headlines,
            npr_links=npr_links,
            chicago_temperature=chicago_temperature,
            last_update=datetime.now().strftime("%b %d, %Y | %I:%M %p"),
        )

        time.sleep(900)

@app.before_request
def activate_job():
    global data_initialized
    if not data_initialized:
        refresh_thread = threading.Thread(target=refresh_data)
        refresh_thread.start()
        data_initialized = True

@app.route('/')
def index():
    data = app.config
    return render_template('index.html', **data)

@app.route('/fetch_npr_content/<path:url>')
def fetch_npr_content(url):
    try:
        response = requests.get(url)
        return response.text, response.status_code, {'Content-Type': 'text/html'}
    except Exception as e:
        return str(e), 500, {'Content-Type': 'text/plain'}

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, app.config['STATIC_FOLDER']),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

if __name__ == '__main__':
    app.run(debug=True, host='192.168.50.214', port=9000)
