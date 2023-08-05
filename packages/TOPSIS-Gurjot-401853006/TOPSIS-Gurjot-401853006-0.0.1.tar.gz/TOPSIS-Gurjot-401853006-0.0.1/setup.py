import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS-Gurjot-401853006",
    version="0.0.1",
    author="Gurjot Singh",
    author_email="gurjot.pruthi@gmail.com",
    description="TOPSIS Analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas'],
    python_requires='>=3.6',
)
