import setuptools
from setuptools import _install_setup_requires

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gherkin2oas", # Replace with your own username
    version="1.0.3",
    author="Tasos Dimanidis",
    author_email="dhmtasos@gmail.com",
    description="A converter from Gherkin to OAS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TasosDhm/gherkin2oas",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=['nltk', 'TextBlob', 'inflect', 'python-dateutil', 'gherkin-official>=4.1.3', 'openapi_spec_validator']
)