import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="topsis_pckg-bansalz1208", # Replace with your own username
    version="0.0.1",
    author="Nikhil Bansal",
    author_email="bansalz1208@gmail.com",
    description="it is package which tells you best value based on the data by using some mathematical calculations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coolestbnslz/topsis_pckg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)