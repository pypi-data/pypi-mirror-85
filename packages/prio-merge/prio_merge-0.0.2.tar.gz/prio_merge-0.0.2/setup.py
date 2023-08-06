import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prio_merge",
    version="0.0.2",
    author="Jonas Wedin",
    author_email="jonas@lechuck.se",
    description="Merge nested dicts according to a few specific rules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ztime/prio-merge",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
