import requests
import json
import string

def do_regex(pattern):
    if isinstance(pattern, str):
        return pattern.split('\\;')[0]
    return pattern

def do_list(data):
    if isinstance(data, str):
        return [do_regex(data)]
    elif isinstance(data, list):
        return [do_regex(pattern) for pattern in data]
    return []

def do_dict(data):
    res = {}
    if isinstance(data, dict):
        for k, v in data.items():
            res[k] = do_regex(v)
    return res

def database():
    base_url = "https://raw.githubusercontent.com/enthec/webappanalyzer/main/src/technologies/"
    
    letters = list(string.ascii_lowercase) + ['_']
    
    signatures = {}
    
    for letter in letters:
        url = f"{base_url}{letter}.json"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()

                for name, tech_data in data.items():
                    rules = {}
                    
                    if 'headers' in tech_data:
                        rules['headers'] = do_dict(tech_data['headers'])
                    if 'cookies' in tech_data:
                        rules['cookies'] = do_dict(tech_data['cookies'])
                    if 'html' in tech_data:
                        rules['html'] = do_list(tech_data['html'])
                    if 'scriptSrc' in tech_data:
                        rules['scripts'] = do_list(tech_data['scriptSrc'])
                    if 'dom' in tech_data:
                        if isinstance(tech_data['dom'], dict):
                            rules['dom'] = list(tech_data['dom'].keys())
                        elif isinstance(tech_data['dom'], str):
                            rules['dom'] = [tech_data['dom']]
                    if 'js' in tech_data:
                        rules['js'] = list(tech_data['js'].keys())
                            
                    if rules:
                        signatures[name] = rules
            else:
                print(f"Status: {resp.status_code}")
        except Exception as e:
            print(f"ERROR : {e}")
            
    with open("signatures.json", "w", encoding="utf-8") as f:
        json.dump(signatures, f, indent=4)
        

if __name__ == "__main__":
    database()