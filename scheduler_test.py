import schedule
import time

def job_that_executes_once():
    print("success")
    return schedule.CancelJob

schedule.every().day.at('22:39').do(job_that_executes_once)

while True:
    schedule.run_pending()
    time.sleep(1)