import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

__author__ = 'aaron'
__date__ = '2020/09/23'

setuptools.setup(
    name="RJUtils",
    version="1.2.2",
    author="Aaron",
    author_email="103514303@qq.com",
    description="RJUtils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StarsAaron",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    install_requires=['bs4', 'pymysql', 'mysql-connector-python', 'pika',
                      'apscheduler', 'sqlalchemy', 'requests', 'redis', 'requests', 'logbook', 'zmq'],
    include_package_data=True,
    zip_safe=True
)
