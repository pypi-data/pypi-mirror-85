import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wyzeapi-JoshMulliken", # Replace with your own username
    version="0.0.1",
    author="Joshua Mulliken",
    author_email="josh.mulliken@hey.com",
    description="Python library to allow interaction with the wyzeapi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoshuaMulliken/wyzeapy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)