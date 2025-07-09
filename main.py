from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

# Helper to load data
def load_prices():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Helper to save data
def save_prices(prices):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(prices, f, ensure_ascii=False, indent=4)

@app.route('/')
def home():
    prices = load_prices()
    return render_template('index.html', prices=prices)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    prices = load_prices()
    if request.method == 'POST':
        item = request.form.get('item')
        price = request.form.get('price')
        if item and price:
            prices[item] = price
            save_prices(prices)
        return redirect('/admin')
    return render_template('admin.html', prices=prices)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
