from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def home():
    prices = load_data()
    return render_template('index.html', prices=prices)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    prices = load_data()
    if request.method == 'POST':
        for item in prices:
            if item in request.form:
                prices[item] = request.form[item]
        save_data(prices)
        return redirect('/admin')
    return render_template('admin.html', prices=prices)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
