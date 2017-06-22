import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__PATH__ = os.path.dirname(__file__)

with open(os.path.join(__PATH__, 'README.rst')) as readme:
    README = readme.read()

with open(os.path.join(__PATH__, 'requirements.txt')) as requirements:
    REQUIREMENTS = requirements.read().split('\n')

setup(
    name='os-tornado',
    version='0.1',
    packages=['os_tornado'],
    include_package_data=True,
    license='MIT License',
    description='A framework to simplify tornado daemon development.',
    long_description=README,
    author='Ozzy',
    author_email='cfhamlet@example.com',
    url='https://github.com/cfhamlet/os-tornado',
    install_requires=REQUIREMENTS,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ])
