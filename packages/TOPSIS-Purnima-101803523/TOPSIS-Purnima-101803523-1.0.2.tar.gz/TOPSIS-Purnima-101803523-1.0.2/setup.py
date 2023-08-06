from setuptools import setup

def readme():
    with open('README.md') as file:
        README = file.read()
    return README

setup(
    name="TOPSIS-Purnima-101803523",
    version="1.0.2",
    description="A Python package to implement TOPSIS.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Purnima Lal",
    author_email="purnimalal009@gmail.com",
    url = 'https://pypi.org/project/TOPSIS-Purnima-101803523',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
    ],
    packages=["src"],
    include_package_data=True,
    install_requires=['numpy',
                      'pandas',
                      'scipy',
                      'tabulate',
     ],
     entry_points={
        "console_scripts": [
            "topsis=src.topsis:main",
        ]
     },
)
