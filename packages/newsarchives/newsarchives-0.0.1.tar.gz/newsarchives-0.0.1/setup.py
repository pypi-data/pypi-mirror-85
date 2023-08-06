import setuptools

setuptools.setup(
    name='newsarchives',
    version='0.0.1',
    author='Aarav Borthakur',
    author_email='gadhaguy13@gmail.com',
    description='The official python client library for the News Archives API',
    long_description='''[Documentation](https://gadhagod.github.io/News-Archives/) |
[GitHub](https://github.com/gadhagod/News-Archives)''',
    long_description_content_type='text/markdown',
    url='https://gadhagod.github.io/News-Archives/',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    scripts=['./bin/news.py'],
    install_requires=[
        'click',
    ],
    python_requires='>=3.6'
)