import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

def fetch_domain(url):
    try:
        response = requests.get(url,headers=HEADERS, verify=False, timeout=10)

        response.raise_for_status()

        cookies_dict = response.cookies.get_dict()

        return {
            "url": url,
            "status_code": response.status_code,
            "html_code": response.text,
            "headers": dict(response.headers),
            "cookies": cookies_dict,
            "error" : None
        }
    except requests.exceptions.Timeout:
        return {"url": url, "status_code": None, "html_code": "", "headers": {}, "cookies": {}, "error": "Timeout"}
        
    except requests.exceptions.ConnectionError:
        return {"url": url, "status_code": None, "html_code": "", "headers": {}, "cookies": {}, "error": "ConnectionError"}
        
    except requests.exceptions.HTTPError as e:
        return {"url": url, "status_code": e.response.status_code, "html_code": "", "headers": {}, "cookies": {}, "error": f"HTTP {e.response.status_code}"}
        
    except requests.exceptions.RequestException as e:
        return {"url": url, "status_code": None, "html_code": "", "headers": {}, "cookies": {}, "error": "UnknownRequestError"}

if __name__ == "__main__":
    res_1 = fetch_domain("https://example.com")
    print(f"URL: {res_1['url']} | Error: {res_1['error']} | Cookies: {res_1['cookies']}")
    
    res_2 = fetch_domain("https://www.wikipedia.org/")
    print(f"URL: {res_2['url']} | Error: {res_2['error']} | Cookies: {res_2['cookies']}")
    
    res_3 = fetch_domain("https://httpstat.us/200?sleep=15000")
    print(f"URL: {res_3['url']} | Error: {res_3['error']} | Cookies: {res_3['cookies']}")