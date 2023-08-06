# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='pysecurebox',
    packages=find_packages(include=['pysecurebox']),
    version='1.0.0',
    description='securebox-py (SecureBox for Python) is a lightweight package to create and manage consistent, '
                'encrypted and authenticated files.',
    keywords=['security', 'files', 'encryption', 'authentication'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],  # https://pypi.org/classifiers/
    author='Simone Perini',
    author_email='perinisimone98@gmail.com',
    license='MIT',
    url='https://github.com/CoffeePerry/securebox-py',
    download_url='https://github.com/CoffeePerry/securebox-py/archive/1.0.0.tar.gz',
    install_requires=['pycryptodomex==3.9.9'],
    setup_requires=['pytest-runner==5.2'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests'
)
