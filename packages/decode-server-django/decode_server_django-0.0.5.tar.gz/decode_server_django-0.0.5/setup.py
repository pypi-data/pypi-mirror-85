from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="decode_server_django",
    version="0.0.5",
    description="Django middleware for Decode Auth",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Django >= 3.0",
        "python-jose ~= 3.2",
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
            "twine>=3.2",
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/usedecode/decode_server/decode_server_django",
    author="Davor Badrov",
    author_email="founders@decodeauth.com"
)
