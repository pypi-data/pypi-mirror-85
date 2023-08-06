from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="TOPSIS-Priyanshu-101803308",
    version="0.0.2",
    description="A Python package implementing TOPSIS technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="Priyanshu Aggarwal",
    author_email="priyanshua098@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["topsis_py"],
    keywords = ['Ranking', 'Topsis'],  
    include_package_data=True,
    install_requires=['scipy',
                      'numpy',
                      'pandas'
     ],
     entry_points={
        "console_scripts": [
            "topsis=topsis_py.topsis:main",
        ]
    },
)
