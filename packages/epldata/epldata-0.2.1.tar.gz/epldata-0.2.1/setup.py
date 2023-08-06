from setuptools import setup, find_packages


setup(
    name="epldata",
    version="0.2.1",
    author="Sarang Purandare",
    author_email="purandare.sarang@gmail.com",
    description="Stuff",
    long_description="You dont gotta know",
    long_description_content_type="text/markdown",
    packages=['epldata'],
    install_requires=[
        'pandas',
        'requests',
        'ipython',     
    ],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)