""" Setup file.
"""
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


setup(name='mailicorn',
    version=0.1,
    description='mailicorn',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ],
    keywords="web services",
    author='',
    author_email='',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'cornice',
        'waitress',
        'sqlalchemy',
        'boto',
        'pylibmc',
        'gevent',
        'imapclient'
    ],
    entry_points = """\
    [entry_points]
      syncworker = mailicorn.workers.sync:main
    [paste.app_factory]
    main = mailicorn:main
    """,
    paster_plugins=['pyramid'],
)
