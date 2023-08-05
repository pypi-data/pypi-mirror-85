from setuptools import setup
import setuptools
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name="AudioFeaturizer",
    version="1.1.0",
    description="Takes audio as input and returns computed features as a dataframe",
    long_description=README,
    long_description_content_type="text/markdown",
    # url="https://github.com/N-Harish/AudioFeaturizer",
    author_email="harishnatarajan24@gmail.com",
    author='Harish-Natarajan',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['librosa', "pandas", "numpy", "matplotlib"],
    python_requires='>=3.7'
)
