from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='beerhawk_behavioural_clusters',
version='0.0.12',
 description='Gaussian distributions',
 packages=['beerhawk_behavioural_clusters'],
 author='Shashi Bhushan Singh',
 author_email='shashi.bhushansingh@ab-inbev.com',
 long_description=long_description,
    long_description_content_type='text/markdown'
 ,zip_safe=False)