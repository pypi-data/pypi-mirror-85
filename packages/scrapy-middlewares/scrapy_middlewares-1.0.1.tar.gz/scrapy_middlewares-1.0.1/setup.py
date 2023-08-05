import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy_middlewares",
    version="1.0.1",
    author="CLannadZSY",
    author_email="zsymidi@gmail.com",
    description="scrapy middleware",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CLannadZSY/scrapy-middlewares",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    py_modules=["scrapy_middlewares"],
)