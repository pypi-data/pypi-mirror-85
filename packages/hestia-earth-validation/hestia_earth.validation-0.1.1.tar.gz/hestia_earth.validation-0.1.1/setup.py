from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()


with open("requirements-ci.txt", "r") as fh:
    REQUIRES = fh.read().splitlines()


setup(
    name='hestia_earth.validation',
    version='0.1.1',
    description='Hestia Data Validation library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Guillaume Royer',
    author_email='guillaumeroyer.mail@gmail.com',
    license='GPL-3.0-or-later',
    url='https://gitlab.com/hestia-earth/hestia-data-validation',
    keywords=['hestia', 'data', 'validation'],
    packages=find_packages(exclude=("tests", "scripts")),
    include_package_data=True,
    python_requires='>=3',
    classifiers=[],
    install_requires=REQUIRES
)
