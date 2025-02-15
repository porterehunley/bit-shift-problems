from setuptools import setup, find_packages

setup(
    name='bitshift',
    version='0.0.1',
    packages=find_packages(where='cli'),
    package_dir={'': 'cli'},
    entry_points={
        'console_scripts': [
            'bitshift=bitshift.main:main',
        ],
    },
    include_package_data=True,
    description='A CLI tool for bit shift problems',
    author='Your Name',
    author_email='your.email@example.com',
    url='http://localhost',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.9',
    install_requires=[
        'mistletoe',
        'functions-framework',
        'Flask>=2.2.1'
    ],
    extras_require={
      "admin": ["firebase_admin"],
    },
) 