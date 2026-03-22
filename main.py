import pandas as pd

def domains_extraction(file_path):
    data_frame = pd.read_parquet(file_path)
    
    print("\nColumns : ", data_frame.columns.tolist())
    print(data_frame.head())

if __name__ == "__main__":
    domains_extraction('domains.parquet')