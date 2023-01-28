from multiprocessing import cpu_count
workers = (cpu_count() * 2) +1
bind = "0.0.0.0:8080"
worker_class = "aiohttp.GunicornUVLoopWebWorker"
preload_app = True
accesslog = "-"
errorlog = "-"
loglevel = "info"
wsgi_app = "app:init_app"
default_proc_name = "AIOHTTP"
proc_name = "AIOHTTP"
