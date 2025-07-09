from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

# تحميل البيانات من ملف JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# حفظ البيانات إلى ملف JSON
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    data = load_data()
    
    if request.method == 'POST':
        product = request.form['product']
        price = request.form['price']
        category = request.form['new_category'] or request.form['category']

        if category not in data:
            data[category] = {}

        data[category][product] = price
        save_data(data)
        return redirect('/admin')
    
    return render_template('admin.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
