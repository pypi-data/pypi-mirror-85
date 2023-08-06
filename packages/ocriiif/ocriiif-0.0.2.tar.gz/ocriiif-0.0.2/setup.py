import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ocriiif",  # Replace with your own username
    version="0.0.2",
    author="Matt McGrattan",
    author_email="matt.mcgrattan@digirati.com",
    description="Library for converting IIIF resources to OCR data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/digirati-co-uk/ocriiif",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["Pillow>=8.0.1", "pytesseract>=0.3.6",
                      "certifi>=2017.4.17", "chardet<4,>=3.0.2",
                      "idna<3,>=2.5", "urllib3<1.27,>=1.21.1",
                      "requests>=2.25.0", "numpy>=1.19.4"],
)
