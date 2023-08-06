from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS_Divyanshu_101803542",
    packages=["TOPSIS_Divyanshu_101803542"],
    version="0.3",
    description="Python package implementing TOPSIS ",
    url="https://github.com/dishu5312/Topsis.git",
    download_url="https://github.com/dishu5312/Topsis/archive/v_01.tar.gz",
    author="Divyanshu Srivastava",
    author_email="dsrivastava_be18@thapar.edu",
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
                      'pandas',
                      'scrapeasy'
    
        ],

)
