# news_webscrap_website

Setting up a virtual environment and installing the necessary dependencies.

Step 1: Install virtualenv (if not already installed)
First, you need to install virtualenv if it's not already installed. Open a terminal and run: sudo apt install virtualenv

Step 2: Verify Installation
Ensure virtualenv is installed correctly: virtualenv --version

Step 3: Create a Virtual Environment
Once virtualenv is installed, create a virtual environment: # For Python 2
virtualenv venv

# For Python 3
virtualenv -p python3 venv

Step 4: Activate the Virtual Environment
Activate the virtual environment: source venv/bin/activate

Step 5: Install Required Packages
With the virtual environment activated, install Flask and Flask-CORS:
pip install Flask Flask-CORS requests beautifulsoup4

Step 6: Run Your Script
Now you should be able to run your script without encountering the ModuleNotFoundError: python lite_cnn_webscrapper.py

Step 7: Deactivate the Virtual Environment (Optional)
When you are done working in your virtual environment, you can deactivate it: deactivate

May need to run: pip install python-dotenv




To set up the LCD, refer to these pages: 
https://wiki.52pi.com/index.php?title=Z-0234

https://www.amazon.com/gp/product/B07S7PJYM6/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1


pi@Thunder:~ $ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 3f 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --   

The address of the LCD running on hostname Thunder at 192.168.50.95 is 3f, as shown in the table above when i2cdetect -y 1 is executed in termimal.