from setuptools import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='browseapi',
    packages=['browseapi'],
    version='0.12.2',
    license='MIT',
    description='eBay Browse API Python client',
    long_description=long_description,
    author='Andrii Matiiash',
    author_email='andmati743@gmail.com',
    url='https://github.com/AverHLV/browseapi',
    download_url='https://github.com/AverHLV/browseapi/archive/0.12.2.tar.gz',
    keywords=['ASYNC', 'BROWSE API', 'CLIENT'],

    install_requires=[
        'aiohttp',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
