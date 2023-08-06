from distutils.core import setup


__version__ = "0.1.0"
URL = "https://github.com/massard-t/django_etna_backend/archive/{}.tar.gz".format(__version__)

setup(
    name="django_etna_backend",
    packages=["django_etna_backend"],
    install_requires=['django', 'etnawrapper'],
    version=__version__,
    description="Django authentication backend for ETNA.",
    author="Theo 'Bob' Massard",
    author_email="massar_t@etna-alternance.net",
    url="https://github.com/tbobm/django_etna_backend",
    download_url=URL,
    keywords=["school", "wrapper", "APIs", "auth", "django"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
    ],
)
