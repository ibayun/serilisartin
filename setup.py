import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ibayun-serilization-pip",
    version="0.0.10",
    author="Ivan Karnyuenka",
    author_email="i.korniyenko@list.ru",
    description="simple serialization and deserialization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ibayun/serilisartin.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
