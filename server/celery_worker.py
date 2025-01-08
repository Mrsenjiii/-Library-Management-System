from celery import Celery

def celery_initilization(app):
    celery = Celery(
        "app",
        backend=app.config['result_backend'],
        broker=app.config['broker_url'],
        enable_utc=False,
        timezone='Asia/Kolkata'
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery