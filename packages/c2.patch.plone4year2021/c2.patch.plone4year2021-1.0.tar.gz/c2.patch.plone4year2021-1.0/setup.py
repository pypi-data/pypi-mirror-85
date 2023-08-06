# -*- coding: utf-8 -*-
"""Installer for the c2.patch.plone4year2021 package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="c2.patch.plone4year2021",
    version="1.0",
    description="This product is monkey patching selected year problem after 2021 for Plone 4",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="Manabu TERADA",
    author_email="terada@cmscom.jp",
    url="https://pypi.python.org/pypi/c2.patch.plone4year2021",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["c2", "c2.patch"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        "setuptools",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = c2.patch.plone4year2021.locales.update:update_locale
    """,
)
