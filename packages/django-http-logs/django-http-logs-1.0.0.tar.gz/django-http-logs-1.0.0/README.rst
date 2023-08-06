================
django_http_logs
================

provide http api for use of logging.handlers.HTTPHandler

save messages into db by asynchoronous,use celery

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'django_http_logs',
    )

2. Include the polls URLconf in your project urls.py like this::

    url(r'logs/', include('django_logs.urls')),

3. Run `python manage.py migrate` to create the http logs  models.

4. Run `python manage.py runserver 0.0.0.0:8080` and run celery worker(config celery self)

5. Start use http logging::

    import time
    from logging.handlers import HTTPHandler
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    host = '127.0.0.1:8080' # django run port
    url = '/logs/apis/'

    handler = HTTPHandler(host, url, method='POST')
    logger.addHandler(handler)
    logger.debug("hello world")

6. Visit http://127.0.0.1:8080/admin to participate in the django_logs.



