import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="homehubRPi",
    version="1.0.0",
    author="Ngoni Mombeshora",
    author_email="nmombeshora3@gmail.com",
    description="A small home hub example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ngonimombeshora/homehubRPi",
    # this should get the tar.gz available
    download_url='https://github.com/ngonimombeshora/homehubRPi/tree/main/dist/homehubRPi-1.0.0.tar.gz',
    keywords=['Smart home', 'IOT', 'Raspberry Pi',
              'pip3', 'python', 'MQTT', 'HTTP/s', 'RESTful'],

    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: System :: Operating System Kernels :: Linux'
    ],
    python_requires='>=3.6',
)
