from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'

# صفحة العرض الرئيسية
@app.route('/')
def home():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return render_template('index.html', data=data)

# صفحة الإدارة
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        category = request.form['category']
        product = request.form['product']
        price = request.form['price']

        # فتح الملف وقراءة البيانات
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}

        # تحديث البيانات حسب التصنيف
        if category not in data:
            data[category] = {}
        data[category][product] = price

        # حفظ البيانات
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return redirect('/admin')

    return render_template('admin.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
