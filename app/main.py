import multiprocessing
import time
from app.scheduler import sayer
from app.tg import tb_listener
from app.vk import vb_listener
from app.db import init_db


if __name__ == '__main__':
    init_db()
    processes = {
        # 'p1': multiprocessing.Process(target=tb_listener, name='listener1'),
        'p2': multiprocessing.Process(target=vb_listener, name='listener2'),
        'p3': multiprocessing.Process(target=sayer, name='sayer'),
    }
    for process in processes.values():
        process.start()
    time.sleep(1)
    tb_listener()
