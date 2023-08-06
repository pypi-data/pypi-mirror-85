from setuptools import setup, find_packages

version = {}
with open("./arango/version.py") as fp:
    exec(fp.read(), version)

with open('./README.rst') as fp:
    description = fp.read()

setup(
    name='python-arango',
    description='Python Driver for ArangoDB',
    long_description=description,
    version=version['__version__'],
    author='Joohwan Oh',
    author_email='joohwan.oh@outlook.com',
    url='https://github.com/joowani/python-arango',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=['requests', 'six', 'requests_toolbelt', 'PyJWT'],
    tests_require=[
        'pytest-cov',
        'python-coveralls',
        'mock',
        'pytest',
    ],
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation :: Sphinx'
    ]
)
