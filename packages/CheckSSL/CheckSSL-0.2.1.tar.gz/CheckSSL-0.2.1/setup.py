from setuptools import setup
import CheckSSL

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="CheckSSL",
    version=CheckSSL.__version__,
    author='Vyacheslav Anzhiganov',
    author_email='hello@anzhiganov.com',
    url='https://gocode.ru/microservices/checkssl-python',
    description="Python script to check on SSL certificates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    packages=[
        'CheckSSL',
    ],
    package_data={
        'CheckSSL': [
        ],
    },
    scripts=[
        'checkssl',
        'checkssl.py'
    ],
    install_requires=[
        'pyopenssl',
        'cryptography',
        'idna',
    ]
)
