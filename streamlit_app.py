import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests


# Function to scrape Dexscreener using Selenium
def scrape_dexscreener_trending():
    """
    Scrapes Dexscreener's trending tokens using Selenium.
    """
    url = "https://dexscreener.com/solana?rankBy=trendingScoreH1&order=desc"

    # Selenium options for headless mode
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Replace 'path_to_chromedriver' with your Chromedriver path
    service = Service("path_to_chromedriver")  # Update this with your Chromedriver path
    driver = webdriver.Chrome(service=service, options=options)

    tokens = []

    try:
        driver.get(url)

        # Locate rows in the trending table (Update selectors based on actual structure)
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


# Function to scrape GMGN using BeautifulSoup
def scrape_gmgn_trending():
    """
    Scrapes GMGN's website for trending tokens.
    """
    url = "https://gmgn.ai/?chain=sol&ref=LbosYDck"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        tokens = []

        # Replace selectors with actual ones from GMGN's page structure
        for item in soup.select(".token-item"):  # Update this selector
            name = item.select_one(".token-name").get_text(strip=True)
            contract = item.select_one(".token-contract").get_text(strip=True)
            liquidity = item.select_one(".token-liquidity").get_text(strip=True)
            volume = item.select_one(".token-volume").get_text(strip=True)
            age = item.select_one(".token-age").get_text(strip=True)
            holders = item.select_one(".token-holders").get_text(strip=True)

            tokens.append({
                "name": name,
                "contract": contract,
                "liquidity": float(liquidity.replace("$", "").replace(",", "")),
                "volume": float(volume.replace("$", "").replace(",", "")),
                "age": float(age.replace(" hours", "")),
                "holders": int(holders.replace(",", ""))
            })

        return tokens
    except Exception as e:
        st.error(f"Error scraping GMGN: {e}")
        return []


# Function to filter tokens based on criteria
def filter_tokens(tokens):
    """
    Filters tokens based on specified criteria:
    - Liquidity < 100,000
    - Volume < 250,000
    - Age ≥ 24 hours
    - Holders ≤ 300
    """
    filtered = []
    for token in tokens:
        if (
            token["liquidity"] < 100000 and
            token["volume"] < 250000 and
            token["age"] >= 24 and
            token["holders"] <= 300
        ):
            filtered.append(token)
    return filtered


# Streamlit App
st.title("Trending Token Scraper")

# Scrape Dexscreener Data
st.header("Dexscreener Trending Tokens")
if st.button("Scrape Dexscreener"):
    dexscreener_tokens = scrape_dexscreener_trending()
    if dexscreener_tokens:
        st.write(f"Found {len(dexscreener_tokens)} tokens on Dexscreener.")
        for token in dexscreener_tokens:
            st.write(token)
    else:
        st.warning("No tokens found or failed to scrape Dexscreener.")

# Scrape GMGN Data
st.header("GMGN Trending Tokens")
if st.button("Scrape GMGN"):
    gmgn_tokens = scrape_gmgn_trending()
    if gmgn_tokens:
        st.write(f"Found {len(gmgn_tokens)} tokens on GMGN.")
        filtered_gmgn = filter_tokens(gmgn_tokens)
        st.write(f"{len(filtered_gmgn)} tokens meet the criteria:")
        for token in filtered_gmgn:
            st.write(f"Name: {token['name']}, Contract: {token['contract']}")
    else:
        st.warning("No tokens found or failed to scrape GMGN.")
