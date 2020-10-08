import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pairs-trading-vjtrost88", # Replace with your own username
    version="0.0.1",
    author="Vince Trost",
    author_email="vincentjosephtrost@gmail.com",
    description="An implementation of je-suis-tm's pairs trading functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vjtrost88/pairs-trading",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
