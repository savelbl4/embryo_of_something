import multiprocessing
import time
from app.scheduler import sayer
from app.tg import tb, tb_listener
from app.vk import vb_listener


if __name__ == '__main__':
    print(f"The Bot is online (id: {tb.get_me().id})...")
    processes = {
        # 'p1': multiprocessing.Process(target=tb_listener, name='listener1'),
        'p2': multiprocessing.Process(target=vb_listener, name='listener2'),
        'p3': multiprocessing.Process(target=sayer, name='sayer'),
    }
    for process in processes.values():
        process.start()
    time.sleep(1)
    tb_listener()
