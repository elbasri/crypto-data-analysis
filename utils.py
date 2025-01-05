import pandas as pd

def load_csv(file_path):
    """Load a CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)

def save_csv(data, file_path):
    """Save a Pandas DataFrame to a CSV file."""
    data.to_csv(file_path, index=False)
