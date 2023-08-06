import setuptools

long_description = """
|PyPI - Version| |Downloads| |Code style: black|

JSON Class Database
===================

En- and decode data-types and classes to JSON-type files or databases.

=====

`View on GitHub`_, `contact Finn`_ or `sponsor this project ❤️`_!

.. _View on GitHub: https://github.com/finnmglas/jcdb
.. _contact Finn: https://contact.finnmglas.com
.. _sponsor this project ❤️: https://sponsor.finnmglas.com

.. |PyPI - Version| image:: https://img.shields.io/pypi/v/jcdb?color=000
   :target: https://pypi.org/project/jcdb/
.. |Downloads| image:: https://img.shields.io/badge/dynamic/json?style=flat&color=000&maxAge=10800&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fjcdb
   :target: https://pepy.tech/project/jcdb
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
"""

setuptools.setup(
    name="jcdb",
    version="0.1.0",
    description="The JSON-Class Database.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="database json",
    url="http://github.com/finnmglas/jcdb",
    author="Finn M Glas",
    author_email="finn@finnmglas.com",
    license="MIT",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [],
    },
    install_requires=[
        "argparse",
    ],
    test_suite="nose.collector",
    tests_require=["nose"],
    include_package_data=True,
    zip_safe=False,
)
