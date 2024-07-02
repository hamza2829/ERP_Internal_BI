import pandas as pd
import numpy as np

# Load the existing Excel file
file_path = "products.csv"
df = pd.read_excel("products.csv")

# Generate synthetic data
num_rows = 1000

# Assuming 'id' is the primary key and needs to be unique
if df['id'].dtype == int:
    start_id = df['id'].max() + 1
else:
    start_id = 1  # Default start if 'id' column is not integer type or is empty

# Generate synthetic data
ids = np.arange(start_id, start_id + num_rows)
names = [f'Product {i}' for i in range(start_id, start_id + num_rows)]
categories = np.random.choice(['Electronics', 'Clothing', 'Home', 'Toys', 'Books'], num_rows)
brands = np.random.choice(['BrandA', 'BrandB', 'BrandC', 'BrandD'], num_rows)
quantities = np.random.randint(1, 100, num_rows)
prices = np.round(np.random.uniform(10, 1000, num_rows), 2)
total_prices = quantities * prices
supplier_ids = np.random.randint(1, 10, num_rows)
dates = pd.date_range(start='2023-01-01', periods=num_rows, freq='D')
customer_ids = np.random.randint(1, 50, num_rows)

# Create a DataFrame with the synthetic data
synthetic_data = pd.DataFrame({
    'id': ids,
    'name': names,
    'category': categories,
    'brand': brands,
    'quantity': quantities,
    'price': prices,
    'total_price': total_prices,
    'supplier_id': supplier_ids,
    'updated_at': dates,
    'customer_id': customer_ids,
    'created_at': dates
})

# Append the synthetic data to the original DataFrame
updated_df = pd.concat([df, synthetic_data], ignore_index=True)

# Save the updated DataFrame to an Excel file
output_file_path = 'products.csv'
updated_df.to_excel(output_file_path, index=False)


