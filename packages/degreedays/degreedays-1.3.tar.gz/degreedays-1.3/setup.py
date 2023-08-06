from distutils.core import setup

def _readme():
    with open('README.txt') as f:
        return f.read()

setup(
    name='degreedays',
    version='1.3',
    description='Degree Days.net API Python Client Library',
    long_description=_readme(),
    long_description_content_type='text/plain',
    author='BizEE Software',
    author_email='info@bizeesoftware.com',
    url='https://www.degreedays.net/api/python',
    # The classifiers list doesn't have Apache 2.0 listed specifically, so we
    # spell it out here.
    license='Apache License, Version 2.0',
    # setup finds modules automatically, but you must list the packages.
    packages=['degreedays', 'degreedays.api', 'degreedays.api.data'],
    classifiers=[ # From https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering'
    ]
)
