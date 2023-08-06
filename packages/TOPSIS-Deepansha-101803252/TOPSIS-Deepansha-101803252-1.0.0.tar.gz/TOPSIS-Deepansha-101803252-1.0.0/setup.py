from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS-Deepansha-101803252",
    version="1.0.0",
    description="A python package for TOPSIS",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Deepansha Goyal",
    author_email="dgoyal_be18@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["TOPSIS-Deepansha-101803252"],
    include_package_data=True,
    install_requires=["requests"],
    
)