# Decode Server Django

A middleware for Django for authenticating requests from [Decode Auth Server](https://decodeauth.com/).


## Installing

Install using pip:

```sh
pip install decode_server_django
```

## A simple example

To integrate your Django app with Decode Auth you need to set the Decode public key and register the middleware with the app.

```python
# in settings.py of your app add the public key
DECODE_PUBLIC_KEY = """-----BEGIN RSA PUBLIC KEY-----
...REDACTED...
-----END RSA PUBLIC KEY-----"""


# And register the middleware
MIDDLEWARE = [
    'decode_server_django.middleware.DecodeAuthMiddleware',
    ...
]
```

Now all the routes will be protected by the middleware and only Decode Auth will be able to call them.

## Developing

To install Decode Server Flask, alogn with the tools you need to develop and run tests, run the following in your virtualenv:

```sh
pip install -e .[dev]
```

## Pushing updates

```sh
# First build the redistributable
python setup.py bdist_wheel sdist

# and then push it to pypi.org
twine upload dist/*
```