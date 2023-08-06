from setuptools import setup
with open("README.md","r") as fh:
    long_description=fh.read()
setup(
    name='TOPSIS-IshaanMarjara-101853028',
    version='0.0.1',
    description='TOPSIS Implementation',
    py_modules=["TOPSIS"],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy>=1.18.1",
        "pandas>=1.0.5"
    ],
    extras_require={
        "dev":[
            "pytest>=3.7",
        ]
    },
    url="",
    author="Ishaan Marjara",
    author_email=""
)
