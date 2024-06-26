import sys
from multiprocessing import cpu_count
from pathlib import Path


def on_starting(_):
    if not Path("config.toml").exists():
        print("файл конфигурации config.toml не найден", file=sys.stderr)
        sys.exit(1)


workers = (cpu_count() * 2) + 1
worker_tmp_dir = "/dev/shm"
bind = "0.0.0.0:8080"
worker_class = "aiohttp.worker.GunicornWebWorker"
preload_app = False
accesslog = "-"
errorlog = "-"
loglevel = "info"
wsgi_app = "main:init_app()"
default_proc_name = "AIOHTTP"
proc_name = "AIOHTTP"
