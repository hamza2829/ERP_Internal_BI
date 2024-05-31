import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    return df

def perform_analysis(df):
    summary_stats = df.describe()

    # Visualize sales distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df['total_price'], bins=30, kde=True)
    plt.title('Distribution of Total Price')
    plt.xlabel('Total Price')
    plt.ylabel('Frequency')

    sales_dist_buffer = BytesIO()
    plt.savefig(sales_dist_buffer, format='png')
    sales_dist_buffer.seek(0)
    sales_dist_plot_data = base64.b64encode(sales_dist_buffer.getvalue()).decode('utf-8')
    plt.close()

    # Plot sales trends over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='created_at', y='total_price', data=df, estimator='sum', errorbar=None)
    plt.title('Total Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Sales Price')

    sales_trend_buffer = BytesIO()
    plt.savefig(sales_trend_buffer, format='png')
    sales_trend_buffer.seek(0)
    sales_trend_plot_data = base64.b64encode(sales_trend_buffer.getvalue()).decode('utf-8')
    plt.close()

    # Group data by id (assuming id is the product ID) and calculate aggregate metrics
    product_metrics = df.groupby('id').agg({
        'quantity': 'sum',
        'total_price': 'sum',
        'price': 'mean'
    })

    # Rename columns for clarity
    product_metrics.rename(columns={'quantity': 'total_quantity', 'total_price': 'total_sales'}, inplace=True)

    # Sort products by total sales in descending order
    top_selling_products = product_metrics.sort_values(by='total_sales', ascending=False).head(10)

    return {
        'summary_stats': summary_stats.to_dict(),
        'sales_dist_plot': sales_dist_plot_data,
        'sales_trend_plot': sales_trend_plot_data,
        'top_selling_products': top_selling_products.to_dict()
    }
