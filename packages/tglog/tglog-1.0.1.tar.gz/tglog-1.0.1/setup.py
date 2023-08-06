import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tglog",
    version="1.0.1",
    author="cypg09",
    author_email="cypg09@protonmail.com",
    description="Log errors in a log.txt file and receive them by telegram.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cypg09/tglog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
