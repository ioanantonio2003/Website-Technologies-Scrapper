from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def fetch_domain(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                ignore_https_errors=True
            )
            page = context.new_page()

            try:
                response = page.goto(url, timeout=15000, wait_until="load")

                page.wait_for_timeout(2000)

                if not response:
                    return {"url": url, "status_code": None, "html_code": "", "headers": {}, "cookies": {},"window_keys": [], "error": "NoResponse"}
                    
                if response.status >= 400:
                     return {"url": url, "status_code": response.status, "html_code": "", "headers": {}, "cookies": {},"window_keys": [], "error": f"HTTP {response.status}"}

                html_code = page.content()
                headers = response.headers
                cookies = context.cookies()
                cookies_dict = {c['name']: c['value'] for c in cookies}
                window_keys = page.evaluate("() => Object.keys(window)")

                return {
                    "url": url,
                    "status_code": response.status,
                    "html_code": html_code,
                    "headers": headers,
                    "cookies": cookies_dict,
                    "window_keys": window_keys,
                    "error": None
                }
            
            except PlaywrightTimeoutError:
                return {"url": url, "status_code": None, "html_code": "", "headers": {}, "cookies": {},"window_keys": [], "error": "Timeout"}
            except Exception as e:
                return {"url": url, "status_code": None, "html_code": "", "headers": {}, "cookies": {},"window_keys": [], "error": "ConnectionError"}
            finally:
                browser.close()

    except Exception as e:
         return {"url": url, "status_code": None, "html_code": "", "headers": {}, "cookies": {},"window_keys": [], "error": "Crash"}

if __name__ == "__main__":
    res_1 = fetch_domain("https://www.wikipedia.org/")
    print(f"URL: {res_1['url']} | Error: {res_1['error']} | Cookies: {len(res_1['cookies'])}")