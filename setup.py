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
        'elasticsearch==6.3.0',
        'elasticsearch-dsl==6.2.1',
        'jseg==0.0.4',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)
