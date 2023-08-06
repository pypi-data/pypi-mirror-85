from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="event-scheduler",
    version="0.0.5",
    author="PhluentMed",
    author_email="PhluentMed@gmail.com",
    description="Non-stop running event scheduler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phluentmed",
    packages=find_packages(),
    keywords='Python Event Scheduler',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
