import os
import pandas as pd

# Define the root data directory
data_dir = "data"
output_file = "data_preview_output.txt"

# Open the output file for writing
with open(output_file, mode='w') as output:
    # Function to preview the first 5 lines of a file
    def preview_file(file_path):
        output.write(f"\n{'='*80}\nPreviewing file: {file_path}\n")
        try:
            # Attempt to load the file with pandas
            data = pd.read_csv(file_path)
            output.write(data.head().to_string() + "\n")  # Write the first 5 rows as a string
        except Exception as e:
            output.write(f"Error reading {file_path}: {e}\n")

    # Recursively walk through the directory and its subdirectories
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".csv"):  # Only process CSV files
                file_path = os.path.join(root, file)
                preview_file(file_path)

    output.write("\nData preview completed.\n")

print(f"Data preview exported to {output_file}")
