from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except Exception as e:
        print("Error loading data:", e)
        products = {}
    return render_template('index.html', products=products)

@app.route('/admin')
def admin():
    return render_template('admin.html')

# هذا الجزء مهم جدًا لتشغيله على Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
