from multiprocessing import cpu_count
workers = (cpu_count() * 10)
bind = "0.0.0.0:8080"
worker_class = "aiohttp.GunicornUVLoopWebWorker"
preload_app = True
accesslog = "-"
errorlog = "-"
loglevel = "info"
wsgi_app = "main:init_app"
default_proc_name = "AIOHTTP"
proc_name = "AIOHTTP"
