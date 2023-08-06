from setuptools import setup, find_packages
from os.path import join, dirname
import ru_sentiment

setup(
    name='ru_sentiment',
    version=ru_sentiment.__version__,
    packages=find_packages(),
    long_description='Short Russian texts sentiment classification',

    install_requires=[
        'torch==1.6.0',
        'transformers==3.0.2',
        'wget==3.2',
        'youtokentome==1.0.6'
    ]
)