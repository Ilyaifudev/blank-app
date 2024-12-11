import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime

# Helper Functions
def fetch_gmgn_data():
    """Scrapes GMGN data for trending tokens."""
    try:
        url = "https://gmgn.com/api/trending"  # Replace with actual API or endpoint
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching GMGN data: {e}")
        return []

def fetch_dexscreener_data():
    """Scrapes Dexscreener data for high-volume tokens."""
    try:
        url = "https://dexscreener.com/api/trending"  # Replace with actual API or endpoint
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching Dexscreener data: {e}")
        return []

def filter_tokens(tokens):
    """Filters tokens based on liquidity, volume, age, and holders."""
    filtered = []
    for token in tokens:
        try:
            liquidity = token.get("liquidity", 0)
            volume = token.get("volume", 0)
            age = token.get("age", 0)  # Assume age is in hours
            holders = token.get("holders", 0)

            if liquidity < 100000 and volume < 250000 and age >= 24 and holders <= 300:
                filtered.append(token)
        except Exception as e:
            st.warning(f"Error filtering token: {e}")
    return filtered

def check_rug_safety(contract_address):
    """Runs the contract address through RugCheck and retrieves the safety report."""
    try:
        url = f"https://rugcheck.xyz/api/check/{contract_address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("minimum_score") in ["Good", "Excellent"]:  # Adjust as per API
            return data
        return None
    except Exception as e:
        st.error(f"Error checking RugCheck for {contract_address}: {e}")
        return None

# Streamlit App
st.title("Token Screener & Rug Safety Checker")

# Button to fetch tokens
if st.button("Fetch Trending Tokens"):
    st.write("Fetching data from GMGN and Dexscreener...")
    gmgn_tokens = fetch_gmgn_data()
    dexscreener_tokens = fetch_dexscreener_data()

    # Combine tokens from both sources
    all_tokens = gmgn_tokens + dexscreener_tokens
    filtered_tokens = filter_tokens(all_tokens)

    st.write(f"Found {len(filtered_tokens)} tokens meeting criteria.")
    for token in filtered_tokens:
        st.write(f"Checking safety for token: {token['name']} ({token['contract']})")
        safety_report = check_rug_safety(token["contract"])
        if safety_report:
            st.success(
                f"Token: {token['name']} ({token['contract']}) - Safety Score: {safety_report['minimum_score']}"
            )
        else:
            st.warning(f"Token {token['name']} did not pass RugCheck criteria.")

# Manual Check
st.subheader("Manual RugCheck")
manual_contract = st.text_input("Enter a contract address:")
if st.button("Run Manual RugCheck"):
    if manual_contract.strip():
        safety_report = check_rug_safety(manual_contract.strip())
        if safety_report:
            st.success(
                f"Contract Address: {manual_contract} - Safety Score: {safety_report['minimum_score']}"
            )
