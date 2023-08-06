import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csv-to-xls-tabs", # Replace with your own username
    version="0.0.2",
    author="vixandrade",
    author_email="vix.andrade21@gmail.com",
    description="Quick python/pandas script to merge multiple CSV files into a xlsx spreadsheet with multiple tabs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vixandrade/csv-to-xls-tabs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)