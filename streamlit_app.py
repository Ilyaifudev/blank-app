import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to scrape Dexscreener for trending tokens
def scrape_dexscreener_trending():
    url = "https://dexscreener.com/solana?rankBy=trendingScoreH1&order=desc"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        tokens = []
        for row in soup.select('tr'):
            columns = row.find_all('td')
            if len(columns) > 1:
                name = columns[0].get_text(strip=True)
                price = columns[1].get_text(strip=True)
                age = columns[2].get_text(strip=True)
                txns = columns[3].get_text(strip=True)
                volume = columns[4].get_text(strip=True)
                liquidity = columns[5].get_text(strip=True)
                mcap = columns[6].get_text(strip=True)

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
        st.error(f"Error scraping Dexscreener: {e}")
        return []

# Function to scrape GMGN for trending tokens
def scrape_gmgn_trending():
    url = "https://gmgn.ai/?chain=sol&ref=LbosYDck"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        tokens = []
        for item in soup.select('.token-item'):
            name = item.select_one('.token-name').get_text(strip=True)
            contract = item.select_one('.token-contract').get_text(strip=True)
            liquidity = item.select_one('.token-liquidity').get_text(strip=True)
            volume = item.select_one('.token-volume').get_text(strip=True)
            age = item.select_one('.token-age').get_text(strip=True)
            holders = item.select_one('.token-holders').get_text(strip=True)

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

# Function to filter tokens based on specified criteria
def filter_tokens(tokens):
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
        filtered_dexscreener = filter_tokens(dexscreener_tokens)
        st.write(f"{len(filtered_dexscreener)} tokens meet the criteria:")
        for token in filtered_dexscreener:
            st.write(f"Name: {token['name']}, Contract: {token['contract']}")
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
