from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    prices = {
        "الذهب": "75,000 SDG",
        "الدولار": "1 USD = 1250 SDG",
        "الذرة الرفيعة": "65,000 SDG",
        "الصمغ العربي": "210,000 SDG",
    }
    return render_template('index.html', prices=prices)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
