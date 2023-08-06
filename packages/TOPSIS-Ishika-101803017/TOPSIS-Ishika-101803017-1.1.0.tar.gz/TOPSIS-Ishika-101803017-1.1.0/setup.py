from setuptools import setup

def readme():
    with open('readme.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS-Ishika-101803017",
    version="1.1.0",
    description="Implementing TOPSIS",
    long_description=readme(),
    long_description_content_type="text/markdown",
    download_url = 'https://github.com/ishikasofat/TOPSIS-Ishika-101803017/archive/1.1.0.tar.gz',
    #long_description=open('README.txt').read(),
    author="Ishika",
    author_email="ishikasofat@gmail.com",
    license="MIT",
    packages=["TOPSIS-Ishika-101803017"],
    install_requires=['numpy','pandas']
)
