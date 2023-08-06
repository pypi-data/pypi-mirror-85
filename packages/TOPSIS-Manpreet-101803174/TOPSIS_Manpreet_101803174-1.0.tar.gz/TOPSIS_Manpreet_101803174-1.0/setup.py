from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="TOPSIS_Manpreet_101803174",
    version="1.0",
    description="A Python package implementing TOPSIS technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Manpreet Singh",
    author_email="msingh_be18@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["TOPSIS_Manpreet_101803174"],
    include_package_data=True,
    install_requires=[
                      'numpy',
                      'pandas'
     ],
     entry_points={
        "console_scripts": [
            "topsis=TOPSIS_Manpreet_101803174.topsis:main",
        ]
     },
)
