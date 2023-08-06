from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS-Misha-101803590",
    version="2.1.1",
    description="Topsis package to calculate the score and rank of a given data.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mishaaggarwal15",
    author="Misha Aggarwal",
    author_email="maggarwal1_be18@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=['topsis_py'],
    include_package_data=True,
    install_requires=["requests","pandas"],
    entry_points={
        "console_scripts": [
            "topsis=topsis_py.ques1:main",
        ]
    },
)
