from flask import Flask, render_template, request
from database import db_session, get_trends, store_ttrends, delete_ttrends, search_trends
# from apscheduler.schedulers.background import BackgroundScheduler
# from wc import createWc


app = Flask(__name__)

# 定期実行
# sched = BackgroundScheduler(timezone="Asia/Tokyo")
# sched.add_job(store_ttrends, "cron", hour="0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23")
# sched.add_job(createWc, "cron", hour="0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23", second="30")
# sched.add_job(delete_ttrends, "cron", hour="23", minute="30", day_of_week="fri")
# sched.start()


@app.route("/")
def index():
    trends = get_trends()
    return render_template("index.html", trends=trends)


@app.route("/res_search", methods=["GET"])
def res_search():
    date = request.args.get("date", "")

    trends = search_trends(date)
    val = len(trends)

    date = date.split("-")
    date = date[0]+"年"+date[1]+"月"+date[2]+"日"
    
    return render_template("res_search.html", date=date, trends=trends, val=val)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(use_reloader=False)
