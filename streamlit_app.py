import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import requests


def enable_request_blocking(driver: WebDriver):
    """
    Enable blocking of network requests to specific URLs.
    """
    driver.execute_cdp_cmd(
        "Network.setBlockedURLs", {"urls": ["https://cdn.segment.com/*"]}
    )
    driver.execute_cdp_cmd("Network.enable", {})


def get_driver():
    """
    Set up Selenium WebDriver with Chromium and Chromedriver.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"  # Path to Chromium binary

    # Set a legitimate User-Agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    )

    # Block unnecessary scripts and ads
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-blink-features=Ads")

    service = Service("/usr/bin/chromedriver")  # Path to Chromedriver binary

    # Enable logging for CDP commands
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}

    driver = webdriver.Chrome(service=service, options=options, desired_capabilities=caps)

    # Block requests to specific third-party domains
    enable_request_blocking(driver)

    return driver


def scrape_dexscreener_trending():
    """
    Scrapes Dexscreener's trending tokens using Selenium.
    """
    url = "https://dexscreener.com/solana?rankBy=trendingScoreH1&order=desc"

    driver = get_driver()
    tokens = []

    try:
        driver.get(url)

        # Locate rows in the trending table
        rows = driver.find_elements(By.CSS_SELECTOR, "tr")
        for row in rows:
            columns = row.find_elements(By.CSS_SELECTOR, "td")
            if len(columns) > 1:
                name = columns[0].text
                price = columns[1].text
                age = columns[2].text
                txns = columns[3].text
                volume = columns[4].text
                liquidity = columns[5].text
                mcap = columns[6].text

                tokens.append({
                    "name": name,
                    "price": price,
                    "age": age,
                    "txns": txns,
                    "volume": volume,
                    "liquidity": liquidity,
                    "mcap": mcap
                })

        return tokens
    except Exception as e:
        st.error(f"Error scraping Dexscreener with Selenium: {e}")
        return []
    finally:
        driver.quit()


# Streamlit App
st.title("Trending Token Scraper")

st.header("Dexscreener Trending Tokens")
if st.button("Scrape Dexscreener"):
    dexscreener_tokens = scrape_dexscreener_trending()
    if dexscreener_tokens:
        st.write(f"Found {len(dexscreener_tokens)} tokens on Dexscreener.")
        for token in dexscreener_tokens:
            st.write(token)
    else:
        st.warning("No tokens found or failed to scrape Dexscreener.")
