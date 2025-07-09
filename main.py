from flask import Flask, render_template, request, redirect, url_for
import json
import os
from urllib.parse import unquote

app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def index():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except Exception as e:
        print("Error loading data:", e)
        products = {}
    return render_template('index.html', products=products)

# صفحة الإدارة لإضافة منتج
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        price = request.form['price']
        image_url = ''  # لا توجد صورة حالياً

        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = {}

        if category not in data:
            data[category] = {}

        data[category][name] = {
            "price": price,
            "image": image_url
        }

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))

    return render_template('admin.html')

# حذف منتج
@app.route('/delete/<category>/<product>')
def delete_product(category, product):
    category = unquote(category)
    product = unquote(product)

    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        if category in data and product in data[category]:
            del data[category][product]

            # احذف الفئة إذا أصبحت فارغة
            if not data[category]:
                del data[category]

            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Delete error:", e)

    return redirect(url_for('index'))

# تشغيل التطبيق
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
