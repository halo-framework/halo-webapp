from io import open

from setuptools import setup
from webfront_service import __version__
# python setup.py sdist --formats=zip
# python setup.py sdist bdist_wheel
# twine upload dist/halolib-0.13.8.tar.gz -r pypitest

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='halo-webapp',
    version=__version__,
    packages=['webfront_service'],
    package_dir={'webfront_service': 'webfront_service'},
    url='https://github.com/halo-framework/halo-webapp',
    license='MIT License',
    author='halo-framework',
    author_email='halo-framework@gmail.com',
    description='this is the Halo webfront_service library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
