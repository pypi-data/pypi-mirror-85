try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="axon-python",
    version="1.0.18",
    author="Axon Edge",
    author_email="info@axonedge.io",
    description="The Python Device SDK for to connected IoT sensors to Axon Edge.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://axonedge.io/",
    packages=['axon'],
    install_requires=[
        "python-dotenv>=0.13.0",
        "nest_asyncio>=1.3.3",
        "AWSIoTPythonSDK>=1.4.8",
        "schema>=0.7",
        "six>=1.5"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.7',
    include_package_data=True,
    package_data={
        '': ['*.ini'],
        'certs': ['*.crt', '*.key', '*.pem']
    },
)
