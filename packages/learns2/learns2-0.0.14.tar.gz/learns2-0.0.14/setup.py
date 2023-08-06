import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="learns2", # Replace with your own username
    version="0.0.14",
    author="Joe Pringle",
    author_email="joe@joepringle.dev",
    description="For use with https://learns2.joepringle.dev",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joechip504/learns2/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'mpyq', 's2protocol'
    ]
)