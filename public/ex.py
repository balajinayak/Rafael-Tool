import pandas as pd

# Sample data as a dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'San Francisco', 'Los Angeles']
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Define the Excel file name
excel_file = 'sample_data.xlsx'

# Save the DataFrame to an Excel file
df.to_excel(excel_file, index=False)  # Set index to False to exclude the index column

print(f'Data saved to {excel_file}')
