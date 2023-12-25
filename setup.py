from setuptools import setup, find_packages

setup(
    name="frontend_developer_agent",
    version="0.0.1",
    packages=find_packages(include=["lcpp"]),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9.13",
    ],
)
