from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS-JASMEHAK-101803163",
    packages=["TOPSIS-JASMEHAK-101803163"],
    version="0.3",
    description="Python package implementing TOPSIS ",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/jasmehakKaur/TOPSIS_PYTHON",
    download_url="https://github.com/jasmehakKaur/TOPSIS_PYTHON/archive/v_0.3.tar.gz",
    author="Jasmehak Kaur",
    author_email="jkaur2_be18@thapar.edu",
    license="MIT",
    keywords = ['TOPSIS','IMPLEMENTATION','PYTHON'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    install_requires=[
                      'numpy',
                      'pandas'
     
    
        ],

)
