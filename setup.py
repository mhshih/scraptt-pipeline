from setuptools import setup, find_packages

setup(
    name='scraptt-pipeline',
    author='amigcamel',
    author_email='amigcamel@gmail.com',
    version='0.0.1',
    description='Scrapy pipeline for scraptt',
    url='github.com/PTT-Corpus/scraptt-pipeline',
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy==1.1.14',
        'psycopg2==2.7.5',
        'cockroachdb==0.2.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
