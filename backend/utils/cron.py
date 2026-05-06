# cron.py

from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os

API_URL = os.getenv("API_URL")


def job():
    try:
        response = requests.get(API_URL, timeout=10)

        if response.status_code == 200:
            print("GET request sent successfully")
        else:
            print(f"GET request failed: {response.status_code}")

    except Exception as e:
        print(f"Error while sending request: {e}")


scheduler = BackgroundScheduler()


def start_scheduler():
    """
    Call this from server.py to start cron safely.
    """
    scheduler.add_job(job, 'cron', minute='*/14')
    scheduler.start()
    print("Cron scheduler started...")