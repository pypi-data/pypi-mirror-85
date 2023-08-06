from setuptools import setup
import CheckSSL

setup(
    name="CheckSSL",
    version=CheckSSL.__version__,
    author='Vyacheslav Anzhiganov',
    author_email='hello@anzhiganov.com',
    url='https://anzhiganov.com',
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
