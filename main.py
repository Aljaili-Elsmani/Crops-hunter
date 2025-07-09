from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    prices = load_data()
    return render_template('index.html', prices=prices)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    data = load_data()
    if request.method == 'POST':
        category = request.form.get('category')
        product = request.form.get('product')
        price = request.form.get('price')

        if category and product and price:
            if category not in data:
                data[category] = {}
            data[category][product] = price
            save_data(data)
            return redirect(url_for('admin'))

    return render_template('admin.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
