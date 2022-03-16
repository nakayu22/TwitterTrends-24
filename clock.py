from database import store_ttrends, delete_ttrends
from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request


def keep_alive():
    print(urllib.request.Request('https://twittertrends-24.herokuapp.com/'))


sched = BlockingScheduler(timezone="Asia/Tokyo")
sched.add_job(keep_alive, 'interval', minutes=20)
sched.add_job(store_ttrends, 'cron', hour='0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22')
sched.add_job(delete_ttrends, 'cron', hour='23', day_of_week='fri')
sched.start()
