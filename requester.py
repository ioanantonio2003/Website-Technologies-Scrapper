import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_domain(url):
    response = requests.get(url, verify=False, timeout=10)

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