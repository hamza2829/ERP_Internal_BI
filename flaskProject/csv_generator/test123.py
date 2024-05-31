import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data into a DataFrame (replace 'products.csv' with your actual data file)
df = pd.read_csv("products.csv")

# Print the column names to verify
print("Column names:", df.columns)
