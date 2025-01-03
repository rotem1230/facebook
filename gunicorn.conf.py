import os

wsgi_app = "main:app"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
timeout = 120

# Access logging
accesslog = "-"
errorlog = "-"
capture_output = True
