import time


def getNow():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_temp():
    t=time.time()
    temp = int(round(t * 1000))
    return temp
