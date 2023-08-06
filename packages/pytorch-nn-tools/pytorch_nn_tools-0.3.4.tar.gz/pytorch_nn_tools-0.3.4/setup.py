#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'torch>=1.0',
    'torchvision',
    'pillow',
    'dataclasses; python_version < "3.7"',
    'tensorboard',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="SergeM",
    author_email='serge-m@users.noreply.github.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Tools for NN creation with Pytorch",
    entry_points={
        'console_scripts': [
            #'pytorch_nn_tools=pytorch_nn_tools.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pytorch_nn_tools',
    name='pytorch_nn_tools',
    packages=find_packages(include=['pytorch_nn_tools', 'pytorch_nn_tools.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/serge-m/pytorch_nn_tools',
    version='0.3.4',
    zip_safe=False,
)
