import setuptools

with open("README.md", "r") as fh: long_description = fh.read()

setuptools.setup( name='mpscreen', version='0.5.5',
                  author="Jakub Klimek",
                  description="A Tool for multiprocess screen manipulation",
                  long_description=long_description,
                  long_description_content_type="text/markdown",
                  packages=setuptools.find_packages(),
                  classifiers=[ "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
                                "Operating System :: POSIX :: Linux", ], )
