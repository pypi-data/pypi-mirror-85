import os
from setuptools import setup, find_packages


setup(
    name='djdzippath',
    version='1.0.0',
    description='zip path',
    long_description='zip path',
    author='heifade',
    author_email='heifade@126.com',
    url='https://heifade.com',
    packages=['src'],
    # data_files=file_data,
    include_package_data=True,
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*",
    install_requires=["requests>=2.24.0"],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)