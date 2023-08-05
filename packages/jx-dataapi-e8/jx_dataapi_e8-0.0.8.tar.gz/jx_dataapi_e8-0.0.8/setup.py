from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
 
# 版本号
VERSION = "0.0.8"
LICENSE = "MIT"
 
setup(
    name='jx_dataapi_e8',
    version=VERSION,
    description=(
        'xjiaxun gateway data api v.E8'
    ),
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='tusky',
    author_email='zj2012yhd@163.com',
    maintainer='tusky',
    maintainer_email='zj2012yhd@163.com',
    license=LICENSE,
    packages=find_packages(),
    platforms=["all"],
    url='http://www.xjiaxun.com',
    install_requires=[  
        "requests==2.21.0",
        "ujson==1.35",
        "moment==0.8.2",
        "scipy==1.4.1"
    ],  
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)