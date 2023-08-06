from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    # Here is the module name.
    name="instainfo",

    # version of the module
    version="0.0.6",

    # Name of Author
    author="Hayden Cordeiro",

    # your Email address
    author_email="cordeirohayden@gmail.com",

    # Small Description about module
    description="Get Profile information of a instagram user",

    long_description=long_description,

    # Specifying that we are using markdown file for description
    long_description_content_type="text/markdown",

    # Any link to reach this module, if you have any webpage or github profile
    url="http://github.com/haydencordeiro",
    packages=['instainfo'],
    install_requires=['requests'],
    # classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False)
