# pykb
Python Knowledge Base app.

## Testing

    nosetest

## Running

    waitress-serve --port=8000 pykb:app

or

    gunicorn pykb:app

or

    waitress-serve --port=8001 pykb:app
    cd ui ; npm start
