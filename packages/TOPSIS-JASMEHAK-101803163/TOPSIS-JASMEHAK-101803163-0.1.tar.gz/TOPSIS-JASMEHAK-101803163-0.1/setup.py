from setuptools import setup

setup(
    name="TOPSIS-JASMEHAK-101803163",
    packages=["TOPSIS-JASMEHAK-101803163"],
    version="0.1",
    description="Python package implementing TOPSIS ",
    url="https://github.com/jasmehakKaur/TOPSIS_PYTHON",
    download_url="https://github.com/jasmehakKaur/TOPSIS_PYTHON/archive/v_0.1.tar.gz",
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
