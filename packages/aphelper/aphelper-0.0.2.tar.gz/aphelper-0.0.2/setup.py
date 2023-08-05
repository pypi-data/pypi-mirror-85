import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("src/aphelper/VERSION", "r") as f:
    version = f.read()

setuptools.setup(
    name="aphelper",
    version=version,
    author="John Carter",
    author_email="jfcarter2358@gmail.com",
    license="MIT",
    description="A Python package to enable declarative definition of argparse CLIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jfcarter2358/aphelper",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    package_dir={'':'src'}
)
