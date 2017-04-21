import multiprocessing


workers = multiprocessing.cpu_count()
bind = "127.0.0.1:5000"
timeout = 1200