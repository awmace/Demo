import time


def get_current_week():
    days = int(time.strftime("%w")) - 1  # 周一到的天数
    if days == -1:
        days = 6
    times = int(time.time()) - 86400 * days + 200
    version = time.strftime('%Y%m%d', time.localtime(times))
    return version



