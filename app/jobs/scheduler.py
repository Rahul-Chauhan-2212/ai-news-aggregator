from apscheduler.schedulers.blocking import BlockingScheduler
from app.jobs.daily_pipeline import run_pipeline

scheduler = BlockingScheduler()


@scheduler.scheduled_job("cron", hour=9)
def job():
    run_pipeline()


scheduler.start()
