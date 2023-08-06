from setuptools import setup, find_packages

version = '0.4.1'
__version__ = version

TESTS_REQUIRE = ["zc.buildout", "zope.testing"]

setup(
    name='z3c.autoinclude',
    version=__version__,
    description="Automatically include ZCML",
    long_description=(open('README.rst').read() + "\n" + open('CHANGES.rst').read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Zope :: 3",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords='zcml automatic',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    url='https://pypi.org/project/z3c.autoinclude',
    license='ZPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.dottedname',
        'zope.interface',
        'zope.configuration',
        'zope.schema>=4.2.0',
    ],
    tests_require=TESTS_REQUIRE,
    extras_require={'test': TESTS_REQUIRE},
    entry_points="""
    [console_scripts]
    autoinclude-test = z3c.autoinclude.tests.tests:interactive_testing_env
    """,
)
