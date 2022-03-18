from database import store_ttrends, delete_ttrends
from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request


# def keep_alive():
#     with urllib.request.urlopen("https://twittertrends-24.herokuapp.com/") as res:
#         print("code:", res.getcode())


sched = BlockingScheduler(timezone="Asia/Tokyo")
# sched.add_job(keep_alive, "interval", minutes=10)
sched.add_job(store_ttrends, "cron", hour="0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23")
sched.add_job(delete_ttrends, "cron", hour="23", minute="30", day_of_week="fri")
sched.start()
