from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="TOPSIS_Shruti_101803512",
    version="1",
    description="A Python pip package to apply topsis approach to rank the entries in a dataset",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Shruti Bansal",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["TOPSIS_Shruti_101803512"],
    include_package_data=True,
    install_requires=["numpy","pandas"],
    entry_points={
        "console_scripts": [
            "TOPSIS_Shruti_101803512=TOPSIS_Shruti_101803512.cli:main",
        ]
    },
) 