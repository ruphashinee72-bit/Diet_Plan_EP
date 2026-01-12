import pandas as pd

def get_clean_data(file_path):
    # Load the CSV normally
    df = pd.read_csv(file_path)
    # Return the dataframe exactly as it is
    return df
