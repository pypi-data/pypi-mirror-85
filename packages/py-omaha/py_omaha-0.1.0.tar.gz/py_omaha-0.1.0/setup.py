from setuptools import find_packages, setup
setup(
    name='py_omaha',
    packages=find_packages(include=['py_omaha']),
    version='0.1.0',
    description='A Python library to interact with the TP-Link Omaha Wifi Access Point management system',
    author='Ilaria Schinina',
    author_email='ilaria@schinina.eu',
    license='MIT',
    install_requires=['requests>=2.17.0'],
    test_suite='tests',
    url='https://bitbucket.org/ilariaschinina/py_omaha/',
    download_url='https://bitbucket.org/ilariaschinina/py_omaha/get/master.tar.gz'
)