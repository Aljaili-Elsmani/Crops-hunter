from flask import Flask, render_template
import json

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

if __name__ == '__main__':
    app.run(debug=True)
