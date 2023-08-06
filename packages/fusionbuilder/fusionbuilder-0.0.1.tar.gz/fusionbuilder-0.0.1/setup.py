from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name = 'fusionbuilder',
    version = '0.0.1',
    url = 'https://github.com/edsu/fusionbuilder/',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['fusionbuilder',],
    install_requires = ['pyparsing'],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    description = "Parse Fusion Page Builder text.",
    long_description=long_description,
    long_description_content_type="text/markdown"
)
