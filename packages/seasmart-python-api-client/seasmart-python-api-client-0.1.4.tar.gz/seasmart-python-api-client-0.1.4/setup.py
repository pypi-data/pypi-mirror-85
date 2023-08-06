import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seasmart-python-api-client",
    version="0.1.4",
    author="Bradley Wogsland",
    author_email="bradley@wogsland.org",
    description="A Python client for the SeaSmart API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SeaSmart/seasmart-python-api-client",
    packages=setuptools.find_packages(exclude=('tests', )),
    platforms=['Any'],
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    keywords='SeaSmart aquaculture IoT',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
