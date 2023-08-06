import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scraper_yt", # Replace with your own username
    version="0.1.0",
    author="Sthitaprajna Mishra",
    author_email="sthitaprajna360@gmail.com",
    description="A package to scrape comments from a YouTube video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sthitaprajna-mishra/scraper_yt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)