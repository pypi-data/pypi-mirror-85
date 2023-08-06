from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setup(
    name="gloriahousing",
    version="0.0.1",
    description="Predicts Median housing value",
    long_description=open("README.txt").read() + "\n\n" + open("CHANGELOG.txt").read(),
    url="",
    author="Gloria Joseph",
    author_email="gloria.joseph@tigeranalytics.com",
    license="MIT",
    classifiers=classifiers,
    keywords="median",
    packages=find_packages(),
    install_requires=[""],
)
