from setuptools import setup

def readme():
    with open('README.md') as file:
        README = file.read()
    return README

setup(
    name="TOPSIS_RATISH_101803004",
    version="1.0.0",
    description="A Python package implementing TOPSIS technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="RATISH JINDAL",
    author_email="JINDALRATISH@gmail.com",
    url = 'https://github.com/gpriya32/TOPSIS-PriyankaGupta-101803006/',
    download_url ='https://github.com/gpriya32/TOPSIS-PriyankaGupta-101803006/archive/1.0.0.tar.gz',
    license="MIT",
    packages=["src"],
    include_package_data=True,
    install_requires=['pip','pypi','setuptools','create_package','numpy','pandas'])