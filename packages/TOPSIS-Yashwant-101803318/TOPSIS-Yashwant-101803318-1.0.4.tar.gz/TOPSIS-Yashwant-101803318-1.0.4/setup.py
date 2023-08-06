import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS-Yashwant-101803318",
    version="1.0.4",
    # package_dir={'':'TOPSIS_Yashwant'},
    py_modules=["TOPSIS"],
    author="Yashwant",
    author_email="yashsn2127@gmail.com",
    description="A Topsis package that takes inputs as CSV and generates scores in results CSV!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/meyash/TOPSIS_101803318",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy>=1.18.1",
        "pandas>=1.0.5"
    ],
)
