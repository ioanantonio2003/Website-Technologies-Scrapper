import json

def results_analyzer(file_path='results.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_technologies = []
    counter = 0
    for site in data:
        if site.get('technologies'):
            counter += 1
        for tech in site.get('technologies', []):
            all_technologies.append(tech['technology'])
    
    unique_techs = set(all_technologies)
    
    print(f"NUMBER OF ALL DETECTIONS : {len(all_technologies)}")
    print(f"NUMBER OF UNIQUE TECHNOLOGIES : {len(unique_techs)}")
    print(f"NUMBER OF SITES WITH TECHNOLOGIES : {counter}")

    for u in unique_techs:
        print(u)

if __name__ == "__main__":
    results_analyzer()