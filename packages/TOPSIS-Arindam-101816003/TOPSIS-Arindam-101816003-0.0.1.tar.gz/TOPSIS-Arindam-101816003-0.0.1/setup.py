from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="TOPSIS-Arindam-101816003",
    version="0.0.1",
    description="Python package for implementing TOPSIS method.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="Arindam Sharma",
    author_email="sharmaarindam200@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    keywords = ["topsis","thapar","data science"],
    install_requires=['numpy',
                      'pandas'
     ],
    entry_points={
        "console_scripts": [
            "topsis=topsis_python.topsis:main",
        ]
    },
)