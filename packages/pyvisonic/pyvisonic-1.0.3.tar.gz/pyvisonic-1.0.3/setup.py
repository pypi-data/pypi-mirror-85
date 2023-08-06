import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvisonic",
    version="1.0.3",
    author="DaveSmegHead",
    author_email="davesmeghead@hotmail.com",
    description="An asyncio python interface library to the visonic alarm panel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davesmeghead/pyvisonic",
    packages=setuptools.find_packages(),
    install_requires=["aconsole", "pyserial_asyncio"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)