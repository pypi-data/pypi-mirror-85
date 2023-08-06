import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_discord",
    version="46.0.0",
    author="TricolorHen061",
    author_email="thisisnotarealemail@pleasedonttrytoemailthis.com",
    description="A simple library to build Discord Bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://simple-discord.000webhostapp.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
