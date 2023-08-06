from setuptools import setup

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='exchange-rate-alert',
    version='0.7',
    description='Create desktop alerts for Transferwise exchange rates',
    long_description=long_description,
    url='https://github.com/paradigmwit/exchange-rate-alert',
    author='Fahd Mohammed Khan',
    author_email='fahd_khan_01@hotmail.com',
    license='MIT',
    zip_safe=False,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'setuptools',
        'click',
        'pypiwin32; sys_platform == "win32"',
        'win10toast; sys_platform == "win32"',
      ],
    entry_points={
        'console_scripts': ['era=ratealert.era:main'],
    },
    python_requires='>=3.6',
)

setup()
