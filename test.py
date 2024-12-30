from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
import random
import time
import uuid
import pymongo
import socket
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os

load_dotenv()

mongoUri = os.getenv('mongoUrii')
# MongoDB setup
client = pymongo.MongoClient(mongoUri)  #MongoDB URI
db = client["twitter_scraper"]  # Database name
collection = db["trending_topics"]  # Collection name

proxy_list = [
    "18.185.169.150:3128",
    "13.36.113.81:3128",
    "13.36.87.105:3128",
    "3.139.242.184:80",
    "44.218.183.55:80",
    "3.136.29.104:80",
    "3.21.101.158:3128",
    "3.130.65.162:3128",
    "13.59.156.167:3128",
    "3.90.100.12:80",
    "103.152.112.120:80",
    "103.152.112.157:80",
    "209.97.150.167:3128",
    "156.231.136.254:8888",
    "114.35.140.157:8080",
    "198.49.68.80:80",
    "162.223.90.130:80",
    "139.162.78.109:8080",
    "51.89.255.67:80",
    "37.187.25.85:80",
    "13.56.192.187:80",
    "13.208.56.180:80",
    "3.71.239.218:3128",
    "35.72.118.126:80",
    "43.202.154.212:80",
    "3.37.125.76:3128",
    "35.76.62.196:80",
    "35.79.120.242:3128",
    "46.51.249.135:3128",
    "43.200.77.128:3128",
    "52.196.1.182:80",
    "3.12.144.146:3128",
    "3.129.184.210:80",
    "54.152.3.36:80",
    "3.141.217.225:80",
    "54.248.238.110:80",
    "63.35.64.177:3128",
    "204.236.137.68:80",
    "173.249.23.14:80",
    "38.54.71.67:80",
    "13.37.89.201:80",
    "13.37.59.99:3128",
    "13.38.176.104:3128",
    "13.36.104.85:80",
    "13.37.73.214:80",
    "38.242.199.124:8089",
    "204.236.176.61:3128",
    "133.18.234.13:80",
    "3.212.148.199:3128",
    "23.247.137.142:80",
    "31.47.58.37:80",
    "184.169.154.119:80",
    "3.126.147.182:80",
    "34.80.240.128:8080",
    "165.232.129.150:80",
    "3.124.133.93:3128",
    "3.127.62.252:80",
    "23.247.136.252:80",
    "3.78.92.159:3128",
    "141.11.103.136:8080",
    "13.38.153.36:80",
    "15.236.106.236:3128",
    "44.195.247.145:80",
    "54.67.125.45:3128",
    "18.228.149.161:80",
    "43.201.121.81:80",
    "54.233.119.172:3128",
    "18.228.198.164:80",
    "52.67.10.183:80",
    "3.127.121.101:80",
    "3.122.84.99:3128",
    "52.73.224.54:3128",
    "189.51.34.116:8056",
    "47.91.120.190:80",
    "27.79.134.66:16000",
    "143.42.66.91:80",
    "172.191.74.198:8080",
    "44.219.175.186:80",
    "47.76.144.139:4145",
    "199.203.152.99:8111",
    "3.123.150.192:80",
    "8.212.168.170:4145",
    "63.143.57.119:80",
    "154.65.39.7:80",
    "175.106.10.227:7878",
    "192.73.244.36:80",
    "45.122.240.154:3128",
    "89.116.34.113:80",
    "190.103.177.131:80",
    "149.202.91.219:80",
    "8.221.138.111:1080",
    "74.48.78.52:80",
    "8.213.222.247:8008",
    "223.205.165.43:8080",
    "211.251.236.253:80"
]

CHROMEDRIVER_PATH = '.\\chromedriver-win64\\chromedriver.exe'  # this is the correct path to ChromeDriver
proxy = random.choice(proxy_list)

# Setting.. up Chrome options with proxy
options = Options()
options.add_argument(f'--proxy-server={proxy}')

# Initializing... ChromeDriver with the selected proxy
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

#Twitter login credentials
TWITTER_USERNAME = os.getenv("TWITTERR_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTERR_PASSWORD")
TWITTER_USER = os.getenv("TWITTERR_USER")

try:
    # Step 1: Open the Twitter login page
    print("Opening Twitter login page...")
    driver.get("https://x.com/login")
    driver.maximize_window()
    time.sleep(8)  # Wait for the login page to load

    # Step 2: Enter username/email
    print("Entering username/email...")
    username_field = driver.find_element(By.NAME, "text")
    username_field.send_keys(TWITTER_USERNAME)
    username_field.send_keys(Keys.RETURN)
    time.sleep(8)  # Wait for the password field to appear

    # Step 3: Enter username if prompted
    print("Checking for username prompt...")
    try:
        username_prompt_field = driver.find_element(By.NAME, "text")
        print("Entering username...")
        username_prompt_field.send_keys(TWITTER_USER)
        username_prompt_field.send_keys(Keys.RETURN)
        time.sleep(8)
    except Exception as e:
        print("Something wrong in checking step 3")

    # Step 4: Enter password
    print("Entering password...")
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(TWITTER_PASSWORD)
    password_field.send_keys(Keys.RETURN)
    time.sleep(8)

    # Step 1: Navigate to the Trending page
    driver.get("https://x.com/explore/tabs/trending")
    print("Navigated to the Trending page...")
    time.sleep(8)  # Allowing time for the content to load

    # Locate all `div` elements containing trends
    all_trending_divs = driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'trend')]")

    # Limit to first 5
    trending_divs = all_trending_divs[:5]
    trending_topics = []
    # Extract and print the text from the first 5 `divs`
    for div in trending_divs:
        lines = div.text.split('\n')
        trending_topics.append(lines[3])
        print(lines[3])

    # Step 12: Create a unique ID for the record
    unique_id = str(uuid.uuid4())

    # Step 13: Get the current IP address
    ip_address = proxy.split(':')[0]  # Using the IP part of the proxy

    # Step 14: date and time
    ist = pytz.timezone('Asia/Kolkata')

    #convert it to IST
    utc_now = datetime.now(pytz.utc)
    ist_time = utc_now.astimezone(ist)

    # Format the IST time
    end_time = ist_time.strftime("%d-%m-%Y %H:%M:%S")

    # Step 15:data to be inserted into MongoDB
    data = {
        "unique_id": unique_id,
        "trend1": trending_topics[0] if len(trending_topics) > 0 else "",
        "trend2": trending_topics[1] if len(trending_topics) > 1 else "",
        "trend3": trending_topics[2] if len(trending_topics) > 2 else "",
        "trend4": trending_topics[3] if len(trending_topics) > 3 else "",
        "trend5": trending_topics[4] if len(trending_topics) > 4 else "",
        "end_time": end_time,
        "ip_address": ip_address
    }

    # Step 16: Insert data into MongoDB
    collection.insert_one(data)
    print(f"Data saved to MongoDB with unique ID: {unique_id}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Step 17: Close the browser
    print("Closing the browser...")
    driver.quit()
