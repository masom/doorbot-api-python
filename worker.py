from doorbot.factory import create_worker_app, create_celery_app


app = create_worker_app('../config_debug.py')
celery = create_celery_app(app.config)
