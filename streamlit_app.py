import streamlit as st
from playwright.sync_api import sync_playwright

def scrape_dexscreener_with_playwright():
    """
    Scrapes Dexscreener's trending tokens using Playwright.
    """
    url = "https://dexscreener.com/solana?rankBy=trendingScoreH1&order=desc"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Intercept and block specific requests
        def block_request(route, request):
            if "cdn.segment.com" in request.url:
                route.abort()
            else:
                route.continue_()

        page.route("**/*", block_request)
        page.goto(url)

        # Scrape data
        rows = page.query_selector_all("tr")
        tokens = []

        for row in rows:
            columns = row.query_selector_all("td")
            if len(columns) > 1:
                name = columns[0].inner_text()
                price = columns[1].inner_text()
                age = columns[2].inner_text()
                txns = columns[3].inner_text()
                volume = columns[4].inner_text()
                liquidity = columns[5].inner_text()
                mcap = columns[6].inner_text()

                tokens.append({
                    "name": name,
                    "price": price,
                    "age": age,
                    "txns": txns,
                    "volume": volume,
                    "liquidity": liquidity,
                    "mcap": mcap
                })

        browser.close()
        return tokens


def scrape_gmgn_with_playwright():
    """
    Scrapes GMGN's website for trending tokens using Playwright.
    """
    url = "https://gmgn.ai/?chain=sol&ref=LbosYDck"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Intercept and block specific requests
        def block_request(route, request):
            if "cdn.segment.com" in request.url:
                route.abort()
            else:
                route.continue_()

        page.route("**/*", block_request)
        page.goto(url)

        # Scrape data
        tokens = []
        rows = page.query_selector_all(".token-item")  # Update this selector based on GMGN's HTML structure

        for row in rows:
            name = row.query_selector(".token-name").inner_text()  # Update selector
            contract = row.query_selector(".token-contract").inner_text()  # Update selector
            liquidity = row.query_selector(".token-liquidity").inner_text().replace("$", "").replace(",", "")
            volume = row.query_selector(".token-volume").inner_text().replace("$", "").replace(",", "")
            age = row.query_selector(".token-age").inner_text().replace(" hours", "")
            holders = row.query_selector(".token-holders").inner_text().replace(",", "")

            tokens.append({
                "name": name,
                "contract": contract,
                "liquidity": float(liquidity),
                "volume": float(volume),
                "age": float(age),
                "holders": int(holders),
            })

        browser.close()
        return tokens


# Streamlit App
st.title("Trending Token Scraper")

# Scrape Dexscreener Data
st.header("Dexscreener Trending Tokens")
if st.button("Scrape Dexscreener"):
    dexscreener_tokens = scrape_dexscreener_with_playwright()
    if dexscreener_tokens:
        st.write(f"Found {len(dexscreener_tokens)} tokens on Dexscreener.")
        for token in dexscreener_tokens:
            st.write(token)
    else:
        st.warning("No tokens found or failed to scrape Dexscreener.")

# Scrape GMGN Data
st.header("GMGN Trending Tokens")
if st.button("Scrape GMGN"):
    gmgn_tokens = scrape_gmgn_with_playwright()
    if gmgn_tokens:
        st.write(f"Found {len(gmgn_tokens)} tokens on GMGN.")
        for token in gmgn_tokens:
            st.write(token)
    else:
        st.warning("No tokens found or failed to scrape GMGN.")
