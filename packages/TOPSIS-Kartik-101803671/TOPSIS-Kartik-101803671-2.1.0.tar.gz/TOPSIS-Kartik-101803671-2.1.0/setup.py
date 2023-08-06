from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS-Kartik-101803671",
    version="2.1.0",
    description="A Python package to get TOPSIS result of any data.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ksharma0408/TOPSIS-Kartik-101803671",
    author="Kartik Sharma",
    author_email="sharma.kartik0408@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["topsis_kartik"],
    include_package_data = True,
    install_requires=["pandas","numpy","scipy"],
    entry_points={
        "console_scripts": [
            "topsis=topsis_kartik.topsis:main",
        ]
    },
)
