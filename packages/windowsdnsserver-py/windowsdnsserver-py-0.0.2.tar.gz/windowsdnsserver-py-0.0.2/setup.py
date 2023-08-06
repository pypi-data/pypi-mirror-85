import setuptools

with open("README.md", "r") as fd:
    long_description = fd.read()

setuptools.setup(
    name="windowsdnsserver-py",
    version="0.0.2",
    author="Bilal Ekrem Harmansa",
    author_email="bilalekremharmansa@gmail.com",
    description="wrapper Python library for Windows Server DnsServer module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bilalekremharmansa/windowsdnsserver-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
