from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="TOPSIS-Akriti-101803608",
    packages=["Topsis_Ranking"],
    version="1.0.2",
    license="MIT",
    description="A Python package to get best alternative available using TOPSIS method.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Akriti Singhal",
    author_email="akritisinghal1663@gmail.com",
    url="https://github.com/Akriti0100/TOPSIS-Akriti-101803608",
    classifiers=[
        "Development Status :: 3 - Alpha",      
        "Intended Audience :: Developers",  
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    install_requires=["pandas"],
    entry_points={
        "console_scripts": [
            "TOPSIS-Akriti-101803608=Topsis_Ranking.topsis:main",
        ]
    },
)