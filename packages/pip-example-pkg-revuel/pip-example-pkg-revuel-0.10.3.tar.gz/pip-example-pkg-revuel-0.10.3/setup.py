import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pip-example-pkg-revuel",
    version="0.10.3",
    author="revuel",
    author_email="revuel22@hotmail.com",
    description="Tutorial to distribute a pip package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/revuel/pip-example-pkg-revule",
    packages=setuptools.find_packages(),
    install_requires=[
        'spacy==2.3.0',
        'en_core_web_sm'
    ],
    dependency_links=['https://github.com/explosion/spacy-models/'
                      'releases/download/en_core_web_sm-2.3.0/en_core_web_sm-2.3.0.tar.gz#egg=en_core_web_sm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
