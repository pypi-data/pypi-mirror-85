import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS_Ayush_Jain_101803690", # Replace with your own username
    version="0.0.4",
    description = 'Implementation of TOPSIS',
    author="Ayush Jain",
    author_email="ayushjain1722@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/TOPSIS_AyushJain",
    packages=["TOPSIS_AyushJain_101803690"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data = True,
    python_requires='>=3.0',
    keywords='topsis pandas rank',
    install_requires=['pandas'],
)