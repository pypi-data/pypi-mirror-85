import setuptools
from epicstore_api import __version__ as version, __author__ as author

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='epicstore_api',
    version=version,
    author=author,
    description='An API wrapper for Epic Games Store written in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SD4RK/epicstore_api',
    license='MIT',
    include_package_data=True,
    install_requires=['requests'],
    download_url=f'https://github.com/SD4RK/epicstore_api/archive/v_{version}.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6'
)