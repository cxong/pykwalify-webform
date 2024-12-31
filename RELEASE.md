# How to make releases

1. Update `pyproject.toml` `version`
2. `uv build` - this creates `dist/pykwalify_webform-X.Y.Z.tar.gz`
3. `twine upload dist/pykwalify_webform-X.Y.Z.tar.gz`