import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    
setuptools.setup(
    name="zjwbox",
    version = "0.2.4",
    author = "zjw",
    author_email="2415528031@qq.com",
    description="a box for package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://zjw.show",
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "wheel", 
        "wget==3.2",
        "lxml==4.6.1", 
        "eventlet==0.29.1",
        "dataclasses",
        "pyppeteer",
        "selenium",
        "nest_asyncio==1.4.1",
        "parsel", 
        "requests", 
        "faker", 
        "openpyxl", 
        "pymongo", 
        "pymysql",
        "redis",
        "jsonpath"
    ]

)
