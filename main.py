import pandas as pd

def normalization(domain):
    return f"https://{domain}"

def get_urls_normalized(file_path):
    data_frame = pd.read_parquet(file_path)

    domains = data_frame['root_domain'].tolist()

    normalized_urls = [normalization(domain) for domain in domains]

    return normalized_urls

if __name__ == "__main__":
    urls = get_urls_normalized('domains.parquet')

    for url in urls[:3]:
        print(url)