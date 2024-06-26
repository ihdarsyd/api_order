from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import random
import pandas as pd

app = Flask(__name__)

def generate_dummy_data(page_size=100):
    data_csv = pd.read_csv('data/order.csv')
    data_dict = data_csv.to_dict('records')
    return data_dict

dummy_data = {}
num_pages = 5
page_size = 10

for page in range(1, num_pages + 1):
    dummy_data[page] = generate_dummy_data(page_size)

@app.route('/api/dummydata', methods=['GET'])
def get_dummy_data():
    page = int(request.args.get('page', 1))
    start_date_str = request.args.get('start_date', (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'))
    end_date_str = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))

    if page < 1 or page > num_pages:
        return jsonify({"message": f"Invalid page number. Must be between 1 and {num_pages}"}), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD format"}), 400

    data_for_page = dummy_data.get(page, [])
    filtered_data = [item for item in data_for_page if start_date <= datetime.strptime(item['order_date'], '%Y-%m-%d %H:%M:%S.%f') <= end_date]

    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(debug=False)
