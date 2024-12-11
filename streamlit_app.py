import streamlit as st
import requests

# Fetch data from Dexscreener
def fetch_token_data(token_address):
    """Fetches data from Dexscreener for a given token."""
    try:
        url = f"https://api.dexscreener.io/latest/dex/tokens/{token_address}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching Dexscreener data: {e}")
        return None

# Filter tokens based on criteria
def filter_tokens(token_data):
    """Filters tokens based on specified criteria."""
    filtered_tokens = []
    if token_data:
        for pair in token_data.get("pairs", []):
            liquidity = pair.get("liquidity", {}).get("usd", 0)
            volume = pair.get("volume", {}).get("usd", 0)
            age_hours = pair.get("pairCreatedAt", 0) / 3600  # Convert seconds to hours
            holders = pair.get("holders", 0)  # Ensure the API provides this field

            if (
                liquidity < 100000
                and volume < 250000
                and age_hours >= 24
                and holders <= 300
            ):
                filtered_tokens.append(pair)
    return filtered_tokens

# RugCheck safety evaluation
def check_rug_safety(contract_address):
    """Runs the contract address through RugCheck and retrieves the safety report."""
    try:
        url = f"https://rugcheck.xyz/api/check/{contract_address}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("minimum_score") in ["Good", "Excellent"]:
            return data
    except Exception as e:
        st.error(f"Error checking RugCheck for {contract_address}: {e}")
    return None

# Streamlit App
st.title("Token Screener & Rug Safety Checker")

# Input for token contract address
token_address = st.text_input("Enter Token Contract Address:")

if st.button("Check Token"):
    if token_address:
        st.write("Fetching token data...")
        token_data = fetch_token_data(token_address)

        if token_data:
            st.write("Filtering tokens based on criteria...")
            filtered_tokens = filter_tokens(token_data)

            if filtered_tokens:
                st.write(f"Found {len(filtered_tokens)} tokens meeting criteria.")
                for token in filtered_tokens:
                    st.write(
                        f"Checking safety for token: {token.get('name', 'Unknown')} ({token_address})"
                    )
                    safety_report = check_rug_safety(token_address)
                    if safety_report:
                        st.success(
                            f"Token: {token.get('name', 'Unknown')} ({token_address}) - Safety Score: {safety_report['minimum_score']}"
                        )
                    else:
                        st.warning(
                            f"Token {token.get('name', 'Unknown')} did not pass RugCheck criteria."
                        )
            else:
                st.warning("No tokens meet the specified criteria.")
        else:
            st.error("Failed to fetch token data.")
    else:
        st.error("Please enter a valid token contract address.")

# Manual RugCheck
st.subheader("Manual RugCheck")
manual_contract = st.text_input("Enter a contract address for manual check:")
if st.button("Run Manual RugCheck"):
    if manual_contract.strip():
        safety_report = check_rug_safety(manual_contract.strip())
        if safety_report:
            st.success(
                f"Contract Address: {manual_contract} - Safety Score: {safety_report['minimum_score']}"
            )
        else:
            st.warning(
                f"Contract Address: {manual_contract} did not pass RugCheck criteria."
            )
    else:
        st.error("Please enter a valid contract address.")
