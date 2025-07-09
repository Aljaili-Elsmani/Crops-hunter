from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    prices = load_data()
    return render_template('index.html', prices=prices)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']

    data = load_data()
    data[name] = price
    save_data(data)

    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
