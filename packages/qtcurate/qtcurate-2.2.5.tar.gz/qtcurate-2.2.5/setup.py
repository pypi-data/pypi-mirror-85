from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="qtcurate",
    version="2.2.5",
    description="Theia SDK Search and Data Extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quantxt/qtcurate-sdk-python",
    author="Milojko Bjelanovic",
    author_email="mbjelanovic@quantxt.com",
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    packages=["qtcurate"],
    include_package_data=True,
    install_requires=['requests', 'smart-open'],
    python_requires='>=3.6'
)
