from setuptools import setup, find_packages

from google_play_scraper import __version__

setup(
    name="async-google-play-scraper",
    python_requires=">=3.3",
    version=__version__,
    url="https://github.com/liorchen/google-play-scraper",
    license="MIT",
    author="Lior Chen",
    author_email="liorchen2@gmail.com",
    description="Async-Google-Play-Scraper provides APIs to easily crawl the Google Play Store"
    " for Python with aiohttp!",
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
    ],
    install_requires=[
          'aiohttp',
    ],
    packages=find_packages(exclude=["tests"]),
    long_description=open("README.md", encoding="UTF-8").read(),
    long_description_content_type="text/markdown",
)
