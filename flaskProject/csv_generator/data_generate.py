import pandas as pd
import numpy as np

# Define dummy data columns
columns = ['date', 'amount', 'quantity', 'category']

# Generate dummy data (you can customize this based on your requirements)
data = {
    'date': pd.date_range(start='2022-01-01', periods=100),  # Generate dates
    'amount': np.random.randint(100, 1000, size=100),         # Random amount values
    'quantity': np.random.randint(1, 10, size=100),           # Random quantity values
    'category': np.random.choice(['A', 'B', 'C'], size=100)   # Random category values
}

# Create DataFrame from dummy data
df = pd.DataFrame(data, columns=columns)

# Save DataFrame to CSV file
csv_file_path = 'dummy_data.csv'
df.to_csv(csv_file_path, index=False)

print(f"CSV file '{csv_file_path}' created successfully.")
