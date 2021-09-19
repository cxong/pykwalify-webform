# How to make releases

1. Update `setup.py` `VERSION`
2. `pipenv run python setup.py sdist` - this creates `dist/pykwalify_webform-X.Y.Z.tar.gz`
3. `twine upload dist/pywkwalify_webform-X.Y.Z.tar.gz`