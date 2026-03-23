from bs4 import BeautifulSoup
import json

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

    lower_headers = {str(k).lower() : str(v).lower() for k, v in headers.items()}

    for name, rules in signatures.items():
        if "headers" in rules:
            for header, value in rules["headers"].items():
                header = header.lower()
                value = value.lower()

                if header in lower_headers:
                    actual_value = lower_headers[header]

                    if value == "" or value in actual_value:
                        found.append({
                            "technology": name,
                            "proof": f"Found in HTTP Headers: {header} = {actual_value}"
                        })

                        break

    return found

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
    script_s = [s.get('src').lower() for s in scripts if s.get('src')]

    html_string = str(soup).lower()

    for name, rules in signatures.items():
        if "scripts" in rules:
            for script in rules["scripts"]:
                script = script.lower()
                for src in script_s:
                    if script in src:
                        found.append({
                            "technology": name,
                            "proof": f"Found in Scripts: src='{src}'"
                        })
                        break
    
        if "html" in rules:
            for html in rules["html"]:
                html = html.lower()
                if html in html_string:
                    found.append({
                        "technology": name,
                        "proof": f"Found HTML signature: '{html}'"
                    })
                    break

    return found


if __name__ == "__main__":
    s = load_json()

    test_headers = {
        "Content-Type": "text/html",
        "Server": "cloudflare-nginx", 
        "X-Shopify-Stage": "production"
    }

    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="generator" content="Joomla! - Open Source Content Management">
        
        <script src="https://connect.facebook.net/en_US/fbevents.js"></script>
    </head>
    <body>
        <div id="root">Hello World</div>
    </body>
    </html>
    """

    res = headers_analyzer(test_headers,s)

    for r in res:
        print(f"Technology : {r['technology']} -> proof : {r['proof']}")

    soup = make_soup(test_html)
    res_2 = html_analyzer(soup,s)

    for r in res_2:
        print(f"Technology : {r['technology']} -> proof : {r['proof']}")
