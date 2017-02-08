from gevent import monkey
monkey.patch_all(socket=False)
import multiprocessing


workers = multiprocessing.cpu_count() * 2 + 1
bind = "127.0.0.1:5000"
timeout = 120