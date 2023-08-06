from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS_SIMRANPREET_101803175",
    version="1.1.1",
    description="A Python package for topsis analysis.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="SIMRANPREET SINGH",
    author_email="ssingh4_be18@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["TOPSIS_SIMRANPREET_101803175"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "TOPSIS_SIMRANPREET_101803175=TOPSIS_SIMRANPREET_101803175.topsis:main",
        ]
    },
)