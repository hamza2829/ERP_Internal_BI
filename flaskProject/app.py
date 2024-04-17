from flask import Flask, request, jsonify
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from io import StringIO

app = Flask(__name__)

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Read CSV data into pandas DataFrame
    df = pd.read_csv(StringIO(file.stream.read().decode("UTF8")), index_col=0)

    # Perform ARIMA modeling
    model = ARIMA(df['amount'], order=(1,1,1))
    results = model.fit()

    # Make predictions
    forecast = results.forecast(steps=10)  # Adjust the number of steps as needed

    # Return forecasted values as JSON response
    return jsonify({'forecast': forecast.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
