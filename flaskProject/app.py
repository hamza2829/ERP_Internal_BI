from flask import Flask, jsonify, send_file
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)


def perform_arima(file_path):
    try:
        # Read CSV file into pandas DataFrame
        df = pd.read_csv(file_path)

        # Perform ARIMA modeling
        model = ARIMA(df['amount'], order=(1, 1, 1))
        results = model.fit()

        # Make predictions (adjust the number of forecast steps as needed)
        forecast = results.forecast(steps=10)

        return forecast.tolist()

    except Exception as e:
        return str(e)


def plot_forecast(forecast_values):
    # Create a plot using matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(forecast_values, marker='o', linestyle='--', color='b')
    plt.title('ARIMA Forecast')
    plt.xlabel('Time Steps')  # Label for the x-axis (time steps)
    plt.ylabel('Forecasted Value')  # Label for the y-axis (forecasted value)
    plt.grid(True)

    # Save the plot to a BytesIO object (in-memory binary stream)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return buffer


@app.route('/predict-arima', methods=['GET'])
def predict_arima():
    # Hardcoded file path (change this to your desired file path)
    file_path = "csv_generator/dummy_data.csv"

    try:
        # Perform ARIMA modeling using the hardcoded file path
        predictions = perform_arima(file_path)

        # Generate a plot of the forecasted values
        # plot_buffer = plot_forecast(predictions)
        print("***************in the try block**************")
        # Return the forecasted values and the plot image as a response
        # return send_file(plot_buffer, mimetype='image/png')
        return jsonify({'forecast': predictions}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
