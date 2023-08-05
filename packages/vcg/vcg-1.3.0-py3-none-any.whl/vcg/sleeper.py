from datetime import datetime
import time
from dateutil.relativedelta import relativedelta
from tqdm import tqdm


def visable_sleep(seconds):
    now_time = datetime.now()
    next_time = now_time + relativedelta(seconds=seconds)
    time_str = next_time.strftime("%Y-%m-%d %H:%M:%S")
    if seconds <= 0:
        print(f"No need to sleep {time_str}")
        return
    pbar = tqdm(range(int(seconds)))

    for i in pbar:
        time.sleep(1)
        pbar.set_description(f"Sleep until {time_str}")


def sleep_delta(d=0, h=0, m=0, s=0):
    now_time = datetime.now()
    next_time = now_time + relativedelta(days=d, hours=h, minutes=m, seconds=s)
    seconds = (next_time - now_time).total_seconds()
    visable_sleep(seconds)


def sleep_before(year=None, month=None, day=None, hour=None, minute=0, second=0):
    now_time = datetime.now()
    now_year = now_time.year
    now_month = now_time.date().month
    now_day = now_time.date().day
    now_hour = now_time.time().hour
    now_data = [now_year, now_month, now_day, now_hour, None, None]
    data = [year, month, day, hour, minute, second]
    flag = True
    for i in range(len(data)):
        d = data[i]
        if d is not None:
            flag = False
        else:
            if not flag:
                raise NotImplementedError()
            else:
                data[i] = now_data[i]
        assert data[i] is not None
    [year, month, day, hour, minute, second] = data
    next_time = datetime(year, month, day, hour, minute, second)
    print(next_time)
    seconds = (next_time - now_time).total_seconds()
    visable_sleep(seconds)
