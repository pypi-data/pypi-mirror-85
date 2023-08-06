import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="TOPSIS-Brahaminder-101803725",
    version='1.0.0',
    description='Implementation of TOPSIS',
    long_description=README,
    long_description_content_type="text/markdown",
    author="Brahaminder Garg",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8"
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=["pandas"],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main"
        ]
    }
)
