import pandas as pd
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

    headers = response['headers']
    soup = make_soup(response['html_code'])

    all = headers_analyzer(headers, signatures) + html_analyzer(soup, signatures)

    unique = [dict(t) for t in {tuple(d.items()) for d in all}]

    return {
        "url": url,
        "technologies": unique,
        "error": None
    }

if __name__ == "__main__":
    signatures = load_json()

    test_url = "https://emag.ro"
    
    res = single_domain(test_url, signatures)
    

    if res["error"]:
        print(f"Error : {res['error']}")
    else:
        print(f"Number of techonolgies :  {len(res['technologies'])} :")
        for tech in res["technologies"]:
            print(f" - {tech['technology']}")
            print(f"   Proof: {tech['proof']}")