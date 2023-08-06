from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(
    name="Topsis-Gaurav-101803221",
    version="0.0.7",
    description="A Python package implementing TOPSIS technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Gaurav",
    author_email="bhandalgaurav1999@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["Topsis_python"],
    include_package_data=True,
    install_requires=['sys',
                      'math',
                      'numpy',
                      'pandas'],
     entry_points={
        "console_scripts": [
            "Topsis-Gaurav-101803221=Topsis_python.101803221_Gaurav:main",
        ]
     },
)
