# pykb

Python Knowledge Base app.

* kbsite - The site configuration.
* pykb - The Python KB App. This needs some refactoring as it is
         currently almost everything.

## Gunicorn

    pip3 install gunicorn
    gunicorn kbsite.wsgi
