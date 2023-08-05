from setuptools import setup, find_packages

setup(
    name="shuttl_geo",
    version="0.0.3",
    description="Geographic helpers",
    url="",
    author="Sherub Thakur",
    author_email="sherub.thakur@shuttl.com",
    license="MIT",
    packages=find_packages(),
    classifiers=["Programming Language :: Python :: 3.7"],
    install_requires=["shapely", "geopy"],
    extras_require={
        "test": ["pytest", "pytest-runner", "pytest-cov", "pytest-pep8"],
        "dev": ["flake8"],
    },
)
