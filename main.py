import pandas as pd
import json
import concurrent.futures
from requester import fetch_domain
from analyzer import load_json, make_soup, headers_analyzer, html_analyzer, cookies_analyzer, js_analyzer

def normalization(domain):
    return f"https://{domain}"

def get_urls_normalized(file_path):
    data_frame = pd.read_parquet(file_path)

    domains = data_frame['root_domain'].tolist()

    normalized_urls = [normalization(domain) for domain in domains]

    return normalized_urls

def single_domain(url, signatures):
    response = fetch_domain(url)

    if response["error"]:
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


    return {
        "url": url,
        "technologies": list(unique.values()),
        "error": None
    }

def all_domains(urls, signatures, max_workers = 3):
    res = []

    with concurrent.futures.ThreadPoolExecutor(max_workers= max_workers) as executor:
        futures = {executor.submit(single_domain, url, signatures): url for url in urls}

        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            try:
                re = future.result()
                res.append(re)
                
                technology_counter = len(re['technologies'])
                status = f"ERROR: {re['error']}" if re['error'] else f"Found {technology_counter} techs"
                print(f"[{i}/{len(urls)}] -> {re['url']} | {status}")

            except Exception as e:
                print(f"ERROR : {e}")
                
    return res



if __name__ == "__main__":
    signatures = load_json()

    urls = get_urls_normalized('domains.parquet')

    res = all_domains(urls, signatures, max_workers=3)

    filename = 'results.json'
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=4, ensure_ascii=False)