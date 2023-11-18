import pandas as pd

# Create a DataFrame without custom column names
data = [
    {"Name": "Alice", "Age": 30},
    {"Name": "Bob", "Age": 25},
    {"Name": "Charlie", "Age": 35}
]

df = pd.DataFrame(data)

# Rename the columns with custom names
custom_col_names = ["Full Name", "Years Old"]
df.columns = custom_col_names

# Specify the Excel file path
excel_file = 'chekd.xlsx'

# Write the DataFrame to an Excel file with custom column names
df.to_excel(excel_file, sheet_name='Sheet1', index=False)

