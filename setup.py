from setuptools import setup
import protocoin


setup(
    name='protocoin',
    version='0.3',
    url='https://github.com/dakk/protocoin',
    license='BSD License',
    author='Davide Gessa, Christian S. Perone',
    author_email='gessadavide@gmail.com, christian.perone@gmail.com',
    description='A pure Python3 bitcoin protocol implementation.',
    long_description='A pure Python3 bitcoin protocol implementation.',
    install_requires=['ecdsa>=0.10'],
    packages=['protocoin'],
    keywords='bitcoin, protocol, blockchain, litecoin, testnet',
    platforms='Any',
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
