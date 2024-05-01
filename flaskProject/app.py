from flask import Flask, jsonify
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
