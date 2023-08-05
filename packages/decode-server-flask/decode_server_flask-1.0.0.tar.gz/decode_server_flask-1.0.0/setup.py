from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="decode_server_flask",
    version="1.0.0",
    description="Flask middleware for Decode Auth",
    py_modules=["decode_server_flask"],
    package_dir={"": "src"},
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
        "flask ~= 1.1",
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
    url="https://github.com/usedecode/decode_server",
    author="Davor Badrov",
    author_email="flask@decodeauth.com"
)
