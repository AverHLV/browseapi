from distutils.core import setup

setup(
    name='browseapi',
    packages=['browseapi'],
    version='0.10',
    license='MIT',
    description='eBay Browse API Python client',
    author='Andrii Matiiash',
    author_email='andmati743@gmail.com',
    url='https://github.com/AverHLV/browseapi',
    download_url='',
    keywords=['ASYNC', 'BROWSE API', 'CLIENT'],

    install_requires=[
        'aiohttp',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
