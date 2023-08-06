import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


python_version = '3.7'


setup(
    name='respice',
    version='0.3',
    author='Mischa Krüger',
    author_email="makmanx64@gmail.com",
    description='Flexible and easy to use non-linear transient electric circuit simulator.',
    keywords='electronics circuit simulation non-linear transient steady-state time-domain',
    url='https://gitlab.com/Makman2/respice',
    project_urls={
        'Bug Tracker': 'https://gitlab.com/Makman2/respice/issues',
        'Source Code': 'https://gitlab.com/Makman2/respice/-/tree/master',
    },
    platforms='any',
    license='MIT',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        f'Programming Language :: Python :: {python_version}',
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Topic :: Scientific/Engineering :: Physics",
    ],

    packages=find_packages(),
    python_requires=f'>={python_version}',
    install_requires=read('requirements.txt').splitlines(),
    tests_require=read('test-requirements.txt').splitlines(),
    setup_requires=read('setup-requirements.txt').splitlines(),
    extras_require={
        'docs': read('docs-requirements.txt').splitlines(),
        'interactive': read('interactive-requirements.txt').splitlines(),
    }
)
