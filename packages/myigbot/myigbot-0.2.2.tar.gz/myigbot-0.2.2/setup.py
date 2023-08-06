import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="myigbot",
    version="0.2.2",
    description="Instagram Private API to like, follow, comment, view & intaract with stories and upload post & stories.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/b31ngD3v/MyIGBot",
    author="Pramurta Sinha (b31ngD3v)",
    author_email="contact.pycoder@gmail.com",
    license="MIT",
    keywords = ['instagram', 'bot', 'api', 'instagram-api', 'instagram-private-api', 'instagram-bot', 'private-api', 'myigbot', 'my-ig-bot'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",    
        "Programming Language :: Python :: 3.9",
        ],
    packages=["myigbot"],
    include_package_data=False,
    install_requires=["requests", "bs4", "numpy", "datetime"],
)
