import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

def fetch_domain(url):
    response = requests.get(url,headers=HEADERS, verify=False, timeout=10)

    response.raise_for_status()

    return {
        "url": url,
        "status_code": response.status_code,
        "html_code": response.text,
        "headers": dict(response.headers) 
    }

if __name__ == "__main__":
    test = "https://example.com"
    res = fetch_domain(test)

    print(f"Status code : {res['status_code']}")
    print(res['html_code'][:100])
    for key, value in list(res['headers'].items())[:3]:
        print(f"{key}: {value}")