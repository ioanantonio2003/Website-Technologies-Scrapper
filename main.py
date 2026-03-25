import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import json
from requester import fetch_domain
from analyzer import load_json, make_soup, headers_analyzer, html_analyzer, cookies_analyzer, js_analyzer

def normalization(domain):
    return f"https://{domain}"

def get_urls_normalized(file_path):
    data_frame = pd.read_parquet(file_path)

    domains = data_frame['root_domain'].drop_duplicates().tolist()

    normalized_urls = [normalization(domain) for domain in domains]

    return normalized_urls


async def single(url, signatures, browser,semaphore):
    async with semaphore:
        response = await fetch_domain(url, browser)
        if response["error"]:
            print(f" -> {url} | ERROR: {response['error']}")
            return {
                "url": url,
                "technologies": [],
                "error": response["error"]
            }
        headers = response['headers']
        cookies = response.get('cookies', {})
        window_keys = response.get('window_keys', [])
        soup = make_soup(response['html_code'])

        found = []
        found.extend(headers_analyzer(headers, signatures))
        found.extend(cookies_analyzer(cookies, signatures))
        found.extend(html_analyzer(soup, signatures))
        found.extend(js_analyzer(window_keys, signatures))

        unique = {}
        for t in found:
            if t['technology'] not in unique:
                unique[t['technology']] = t

        technology_counter = len(unique)
        print(f" -> {url} | Found {technology_counter} techs")

        return {
            "url": url,
            "technologies": list(unique.values()),
            "error": None
        }

async def main():
    signatures = load_json()

    urls = get_urls_normalized('domains.parquet')

    semaphore = asyncio.Semaphore(3)
    res = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        tasks = [single(url, signatures, browser,semaphore) for url in urls]
        res = await asyncio.gather(*tasks)
        await browser.close()

    filename = 'results.json'
    
    with open(filename, 'w', encoding='utf-8') as f:
            json.dump(res, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(main())