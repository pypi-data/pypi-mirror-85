import setuptools
with open("README.md", "r") as fh:
    long = fh.read()
setuptools.setup(
    name="Topsis-Nikhil-101803670",
    packages = ['topsis_pckg'],
    version="0.0.6",
    author="Nikhil Bansal",
    author_email="bansalz1208@gmail.com",
    description="it is package which tells you best value based on the data by using some mathematical calculations",
    long_description=long,
    long_description_content_type="text/markdown",
    url="https://github.com/coolestbnslz/topsis_pckg",
    install_requires=['pandas','numpy==1.19.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)