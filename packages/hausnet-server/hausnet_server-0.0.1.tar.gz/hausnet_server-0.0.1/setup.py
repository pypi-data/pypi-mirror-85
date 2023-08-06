import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hausnet_server",
    version="0.0.1",
    author="Louis Calitz",
    author_email="louis@hausnet.io",
    description="A server for the HausNet protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liber-tas/hausmon-client",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'paho-mqtt',
        'aioreactive',
        'janus'
    ]
)
