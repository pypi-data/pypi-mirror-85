import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="cadmean-rpckit",
    version="0.2",
    author="Aleksei Kritskov",
    author_email="krickov.aleksey@cadmean.ru",
    description="A cadRPC client library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cadmean-ru/pythonRPCKit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)