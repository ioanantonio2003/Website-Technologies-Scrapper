import pandas as pd
import concurrent.futures
from requester import fetch_domain
from analyzer import load_json, make_soup, headers_analyzer, html_analyzer

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
    soup = make_soup(response['html_code'])

    all = headers_analyzer(headers, signatures) + html_analyzer(soup, signatures)

    unique = [dict(t) for t in {tuple(d.items()) for d in all}]

    return {
        "url": url,
        "technologies": unique,
        "error": None
    }

def all_domains(urls, signatures, max_workers = 10):
    res = []

    with concurrent.futures.ThreadPoolExecutor(max_workers= max_workers) as executor:
        futures = {executor.submit(single_domain, url, signatures): url for url in urls}

        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            try:
                re = future.result()
                res.append(re)
                
                print(f"[{i}/{len(urls)}]  -> {re['url']}")

            except Exception as e:
                print(f"ERROR : {e}")
                
    return res



if __name__ == "__main__":
    signatures = load_json()

    urls = get_urls_normalized('domains.parquet')

    urls_test = urls[:20]

    res = all_domains(urls_test, signatures, max_workers=10)

    print(f"{len(res)} domains")