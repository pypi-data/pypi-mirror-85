import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='BBCHeadlines',
    version='4.1',
    author='Aarav Borthakur',
    author_email='gadhaguy13@gmail.com',
    description='A python package to get news from BBC.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gadhagod/BBCHeadlines',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'feedparser',
    ],
    python_requires='>=3.6'
)
