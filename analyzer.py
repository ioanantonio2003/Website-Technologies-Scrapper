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

if __name__ == "__main__":
    s = load_json()

    test_headers = {
        "Content-Type": "text/html",
        "Server": "cloudflare-nginx", 
        "X-Shopify-Stage": "production"
    }

    res = headers_analyzer(test_headers,s)

    for r in res:
        print(f"Technology : {r['technology']} -> proof : {r['proof']}")