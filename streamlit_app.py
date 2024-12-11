import streamlit as st
from bs4 import BeautifulSoup
import requests


def scrape_dexscreener():
    """
    Scrapes Dexscreener's trending tokens using requests and BeautifulSoup.
    """
    url = "https://dexscreener.com/solana?rankBy=trendingScoreH1&order=desc"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        tokens = []

        # Locate the table rows containing token data
        rows = soup.select("tr")  # Update selector based on the actual table structure
        for row in rows:
            columns = row.find_all("td")
            if len(columns) > 1:
                name = columns[0].text.strip()
                price = columns[1].text.strip()
                age = columns[2].text.strip()
                txns = columns[3].text.strip()
                volume = columns[4].text.strip()
                liquidity = columns[5].text.strip()
                mcap = columns[6].text.strip()

                tokens.append({
                    "name": name,
                    "price": price,
                    "age": age,
                    "txns": txns,
                    "volume": volume,
                    "liquidity": liquidity,
                    "mcap": mcap,
                })

        return tokens
    except Exception as e:
        st.error(f"Error scraping Dexscreener: {e}")
        return []


def scrape_gmgn():
    """
    Scrapes GMGN's trending tokens using requests and BeautifulSoup.
    """
    url = "https://gmgn.ai/?chain=sol&ref=LbosYDck"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        tokens = []

        # Update selectors to match GMGN's HTML structure
        rows = soup.select(".token-item")  # Update based on actual HTML
        for row in rows:
            name = row.select_one(".token-name").text.strip()
            contract = row.select_one(".token-contract").text.strip()
            liquidity = row.select_one(".token-liquidity").text.strip().replace("$", "").replace(",", "")
            volume = row.select_one(".token-volume").text.strip().replace("$", "").replace(",", "")
            age = row.select_one(".token-age").text.strip().replace(" hours", "")
            holders = row.select_one(".token-holders").text.strip().replace(",", "")

            tokens.append({
                "name": name,
                "contract": contract,
                "liquidity": float(liquidity),
                "volume": float(volume),
                "age": float(age),
                "holders": int(holders),
            })

        return tokens
    except Exception as e:
        st.error(f"Error scraping GMGN: {e}")
        return []


# Streamlit App
st.title("Trending Token Scraper")

# Scrape Dexscreener Data
st.header("Dexscreener Trending Tokens")
if st.button("Scrape Dexscreener"):
    dexscreener_tokens = scrape_dexscreener()
    if dexscreener_tokens:
        st.write(f"Found {len(dexscreener_tokens)} tokens on Dexscreener.")
        for token in dexscreener_tokens:
            st.write(token)
    else:
        st.warning("No tokens found or failed to scrape Dexscreener.")

# Scrape GMGN Data
st.header("GMGN Trending Tokens")
if st.button("Scrape GMGN"):
    gmgn_tokens = scrape_gmgn()
    if gmgn_tokens:
        st.write(f"Found {len(gmgn_tokens)} tokens on GMGN.")
        for token in gmgn_tokens:
            st.write(token)
    else:
        st.warning("No tokens found or failed to scrape GMGN.")
