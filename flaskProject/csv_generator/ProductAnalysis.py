import pandas as pd
import base64

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    return df

import numpy as np

def perform_analysis(df):
    # Generate summary statistics
    summary_stats = df.describe().replace({np.nan: None}).to_dict()

    # Group data by id (assuming id is the product ID) and calculate aggregate metrics
    product_metrics = df.groupby('id').agg({
        'quantity': 'sum',
        'total_price': 'sum',
        'price': 'mean'
    })

    # Rename columns for clarity
    product_metrics.rename(columns={'quantity': 'total_quantity', 'total_price': 'total_sales'}, inplace=True)

    # Replace NaN values with None for JSON serialization
    product_metrics = product_metrics.replace({np.nan: None})

    # Sort products by total sales in descending order
    top_selling_products = product_metrics.sort_values(by='total_sales', ascending=False).head(10)

    return {
        'summary_stats': summary_stats,
        'top_selling_products': top_selling_products.to_dict()
    }
