from bs4 import BeautifulSoup
import json
import re

def load_json(file_path = 'signatures.json'):
    with open(file_path, "r", encoding="UTF-8") as f:
        return json.load(f)

def make_soup(html_content):
    if not html_content:
        return None
    
    soup = BeautifulSoup(html_content, 'html.parser')

    return soup

def headers_analyzer(headers, signatures):
    found = []

    lower_headers = {str(k).lower() : str(v) for k, v in headers.items()}

    for name, rules in signatures.items():
        if "headers" in rules:
            for header, pattern in rules["headers"].items():
                header = header.lower()

                if header in lower_headers:
                    actual_value = lower_headers[header]
                    
                    try:
                        if pattern == "" or re.search(pattern, actual_value, re.IGNORECASE):
                            found.append({
                                "technology": name,
                                "proof": f"Found in HTTP Headers: {header} matched regex  {actual_value}"
                            })

                            break
                    except re.error:
                        pass

    return found

def cookies_analyzer(cookies, signatures):
    found = []

    lower_cookies = {str(k).lower() : str(v) for k, v in cookies.items()}

    for name,rules in signatures.items():
        if "cookies" in rules:
            for cookie_name, pattern in rules["cookies"].items():
                cookie_name = cookie_name.lower()

                if cookie_name in lower_cookies:
                    actual_value = lower_cookies[cookie_name]

                try:
                    if pattern == "" or re.search(pattern, actual_value, re.IGNORECASE):
                        found.append({
                            "technology" : name,
                            "proof": f"Found in Cookies: {cookie_name} matched regex {pattern}"
                        })
                        break
                except re.error:
                    pass


def html_analyzer(soup, signatures):
    found = []

    if not soup:
        return found
    
    meta_tags = soup.find_all('meta',attrs={'name': lambda x: x and x.lower() == 'generator'}
                              )
    for meta in meta_tags:
        name = meta.get('content')
        if name:
            found.append({
                "technology": name.strip(),
                "proof": f"Found in HTML: <meta name=\"generator\" content=\"{name}\">"
            })

    scripts = soup.find_all('script')
    script_s = [s.get('src') for s in scripts if s.get('src')]

    html_string = str(soup)

    for name, rules in signatures.items():
        if "scripts" in rules:
            for pattern in rules["scripts"]:
                for src in script_s:
                    try:
                        if re.search(pattern, src, re.IGNORECASE):
                            found.append({
                                "technology": name,
                                "proof": f"Found in Scripts: {src} matched regex {pattern}"
                            })
                            break
                    except re.error:
                        pass
    
        if "html" in rules:
            for pattern in rules["html"]:
                try:
                    if re.search(pattern, html_string, re.IGNORECASE):
                        found.append({
                            "technology": name,
                            "proof": f"Found HTML signature matching regex {pattern}"
                        })
                        break
                except re.error:
                    pass

    return found


if __name__ == "__main__":
   print("******")
