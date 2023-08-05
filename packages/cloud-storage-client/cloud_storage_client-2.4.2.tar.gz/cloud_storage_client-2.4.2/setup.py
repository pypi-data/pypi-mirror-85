import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "cloud_storage_client",
    version = "2.4.2",
    author = "Pablo Aguirre",
    author_email = "paguirrerubio@gmail.com",
    license = "MIT",
    url = "https://pypi.org/project/cloud-storage-client/",
    packages=['cloud_storage_client'],
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=[
        'botocore==1.12.250',
        'boto3==1.9.250',
        'google-api-core==1.22.4',
        'google-cloud-core==1.4.3',
        'google-cloud-storage==1.32.0',
        'azure-storage-blob==12.3.0',
        'pysftp==0.2.9',
        'ssh-agent-setup==1.0.1'
    ],
)
