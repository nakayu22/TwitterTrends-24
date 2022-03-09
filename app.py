from flask import Flask, render_template
from database import db_session, get_trends
from apscheduler.schedulers.background import BackgroundScheduler
from getTrends import store_ttrends


app = Flask(__name__)

sched = BackgroundScheduler(daemon=True, timezone="Asia/Tokyo")
sched.add_job(store_ttrends, 'cron', hour='0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22')
sched.start()


@app.route("/")
def index():
    trends = get_trends()
    return render_template("index.html", trends=trends)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(use_reloader=False)