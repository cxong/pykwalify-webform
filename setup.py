import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
VERSION = "0.1.1"

setup(
    name="pykwalify_webform",
    packages=find_packages(exclude=("tests",)),
    version=VERSION,
    license="MIT",
    description="Generate webforms based on YAML schema with pykwalify",
    long_description=README,
    long_description_content_type="text/markdown",
    author="congusbongus",
    author_email="congusbongus@gmail.com",
    url="https://github.com/cxong/pykwalify-webform",
    download_url=f"https://github.com/cxong/pykwalify-webform/archive/refs/tags/{VERSION}.tar.gz",
    keywords=["pykwalify", "webform", "template"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    install_requires=["jinja2", "pykwalify", "click"],
    entry_points={
        "console_scripts": [
            "pykwalify_webform=pykwalify_webform.__main__:main",
        ]
    },
    zip_safe=False,
)
