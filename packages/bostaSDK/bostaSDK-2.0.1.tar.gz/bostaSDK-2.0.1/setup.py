from setuptools import setup, Extension, find_packages

setup(
    name='bostaSDK',
    version='2.0.1',
    author='bosta',
    author_email='sdk@bosta.com',
    scripts=[],
    packages = find_packages(),
    keywords=["bosta", "client-sdk", "api", "api-integration"],
    url= 'https://pypi.org/project/bostaSDK/',
    license='LICENSE',
    description='Bosta Python SDK',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'requests'
    ],
    python_requires='>=3.6',
)
