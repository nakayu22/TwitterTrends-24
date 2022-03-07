from flask import Flask, render_template
from database import get_trends

app = Flask(__name__)

@app.route("/")
def index():
    trend = get_trends()
    return render_template("index.html", trend=trend)