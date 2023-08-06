import setuptools, sys

with open("README.rst", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="orator_validator",
    version="0.3.2",
    author="Alfonso Villalobos",
    author_email="alfonso@codepeat.com",
    license='MIT',
    description="Orator Validator provides the best Model implement validation for Orator",
    long_description=long_description,
    packages=setuptools.find_packages(),
    py_modules=['orator_validator'],
    scripts=['orator_validator.py'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7'
)
