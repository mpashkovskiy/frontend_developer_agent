from setuptools import setup, find_packages

setup(
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9.13",
    ],
    entry_points={
        'console_scripts': [
            'run = frontend_developer_agent.main:main',
        ],
    },
    name="frontend_developer_agent",
    packages=find_packages(include=["frontend_developer_agent"]),
    version="0.0.1",
)
