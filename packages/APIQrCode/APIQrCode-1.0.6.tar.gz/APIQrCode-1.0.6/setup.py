# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='APIQrCode',
    version='1.0.6',
    description='SDK API QrCode Python Cielo',
    author='Júnior Carvalho',
    author_email='joseadolfojr@gmail.com',
    url='https://github.com/Jeitto/sdk-qrcode-cielo.git',
    keywords='cielo qrcode',
    install_requires=['requests', 'pycrypto'],
    license='MIT',
    packages=find_packages(),
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
    ),
    python_requires='>=3.0',
)
