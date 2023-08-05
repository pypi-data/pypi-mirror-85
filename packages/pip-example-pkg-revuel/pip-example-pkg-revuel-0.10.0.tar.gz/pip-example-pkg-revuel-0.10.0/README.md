# Pip example package 

[![Build Status](https://travis-ci.org/revuel/pip-example-pkg-revuel.svg?branch=master)](https://travis-ci.org/revuel/pip-example-pkg-revuel) 
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=revuel_pip-example-pkg-revuel&metric=coverage)](https://sonarcloud.io/dashboard?id=revuel_pip-example-pkg-revuel)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=revuel_pip-example-pkg-revuel&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=revuel_pip-example-pkg-revuel)
[![PyPI](https://img.shields.io/pypi/v/pip-example-pkg-revuel?color=purple&label=latest)](https://pypi.org/project/pip-example-pkg-revuel/)
[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)

---

[Tutorial about how to distribute pip packages](https://packaging.python.org/tutorials/packaging-projects/)

## Raw CLI
**Dependencies**

`pip install --upgrade setuptools wheel`

`pip install --upgrade twine`

**Build**

`python setup.py sdist bdist_wheel`

**Upload**

`twine upload  dist/*`

---

&#9989; Here a minion just to make this file more friendly

[<img src="https://upload.wikimedia.org/wikipedia/commons/f/fe/Minion_%28example%29.svg" width="100"/>](image.png)
