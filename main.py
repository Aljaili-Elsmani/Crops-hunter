from flask import Flask, render_template, request, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# إنشاء مجلد لحفظ الصور
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

# صفحة الإدارة (إضافة منتج)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        price = request.form['price']
        image_file = request.files['image']

        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_url = '/' + image_path  # لتحميل الصورة في الموقع
        else:
            image_url = ''  # لا توجد صورة

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

        return redirect(url_for('admin'))

    return render_template('admin.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
