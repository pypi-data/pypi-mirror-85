import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dockter",  # Replace with your own username
    version="0.1.7",
    author="Samuel Mignot",
    description=
    "A package to create dockerfiles for jupyter notebooks to ensure compatibility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sjmignot/dockter.nb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'dockter = dockter.dockter:main',
        ],
    },
    python_requires='>=3.6')
