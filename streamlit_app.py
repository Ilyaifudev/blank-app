def scrape_gmgn_with_proxy():
    """
    Scrapes GMGN's trending tokens using a proxy with enhanced headers and retry mechanism.
    """
    import random
    from tenacity import retry, stop_after_attempt, wait_fixed

    url = "https://gmgn.ai/?chain=sol&ref=LbosYDck"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
    }

    # Rotate proxies
    proxies_list = [
        "http://160.223.163.31:8080",
        "http://165.227.44.38:3128",
    ]
    proxies = {
        "http": random.choice(proxies_list),
        "https": random.choice(proxies_list),
    }

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def fetch_data():
        response = requests.get(url, headers=headers, proxies=proxies, verify=False)
        response.raise_for_status()
        return response

    try:
        response = fetch_data()

        soup = BeautifulSoup(response.text, "html.parser")
        tokens = []

        # Update selectors to match GMGN's HTML structure
        rows = soup.select(".token-item")  # Update based on actual HTML
        for row in rows:
            name = row.select_one(".token-name").text.strip() if row.select_one(".token-name") else "N/A"
            contract = row.select_one(".token-contract").text.strip() if row.select_one(".token-contract") else "N/A"
            liquidity = row.select_one(".token-liquidity").text.strip().replace("$", "").replace(",", "") if row.select_one(".token-liquidity") else "0"
            volume = row.select_one(".token-volume").text.strip().replace("$", "").replace(",", "") if row.select_one(".token-volume") else "0"
            age = row.select_one(".token-age").text.strip().replace(" hours", "") if row.select_one(".token-age") else "0"
            holders = row.select_one(".token-holders").text.strip().replace(",", "") if row.select_one(".token-holders") else "0"

            tokens.append({
                "name": name,
                "contract": contract,
                "liquidity": float(liquidity),
                "volume": float(volume),
                "age": float(age),
                "holders": int(holders),
            })

        return tokens
    except requests.exceptions.RequestException as e:
        st.error(f"Error scraping GMGN with Proxy: {e}")
        return []
