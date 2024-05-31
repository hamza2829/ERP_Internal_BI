from flask import Flask, jsonify, request
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from flask_cors import CORS

from csv_generator.ProductAnalysis import load_data, perform_analysis

app = Flask(__name__)

# Enable CORS for all origins (for development purposes, adjust as needed for production)
CORS(app, resources={r"/*": {"origins": "*"}})

def perform_arima(df):
    try:
        # Perform ARIMA modeling
        model = ARIMA(df['total_price'], order=(1, 1, 1))  # Assuming 'total_price' is the column of interest
        results = model.fit()

        # Make predictions (adjust the number of forecast steps as needed)
        forecast = results.forecast(steps=10)
        return forecast.tolist()

    except Exception as e:
        return str(e)

@app.route('/predict-arima', methods=['GET'])
def predict_arima():
    # Hardcoded file path (change this to your desired file path)
    file_path = "csv_generator/products.csv"

    try:
        # Read CSV file into pandas DataFrame
        df = pd.read_csv(file_path)

        # Perform ARIMA modeling using the DataFrame
        predictions = perform_arima(df)

        # Return the forecasted values as a JSON response
        return jsonify({'forecast': predictions}), 200

    except FileNotFoundError as e:
        return jsonify({'error': f'File not found: {str(e)}'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze-products', methods=['GET'])
def analyze_product():
    product_name = request.args.get('product_name').strip().lower()
    file_path = 'csv_generator/products.csv'
    try:
        df = load_data(file_path)

        # Normalize product names for comparison
        df['name'] = df['name'].str.strip().str.lower()

        print("*****************Data******************")
        print(df)

        product_df = df[df['name'] == product_name]

        if product_df.empty:
            return jsonify({'error': 'Product not found'}), 404

        analysis_results = perform_analysis(product_df)
        return jsonify(analysis_results)
    except FileNotFoundError as e:
        return jsonify({'error': f'File not found: {str(e)}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/products', methods=['GET'])
def get_products():
    file_path = 'csv_generator/products.csv'
    try:
        df = pd.read_csv(file_path)
        products = df['name'].unique().tolist()
        return jsonify({'products': products}), 200
    except FileNotFoundError as e:
        return jsonify({'error': f'File not found: {str(e)}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
