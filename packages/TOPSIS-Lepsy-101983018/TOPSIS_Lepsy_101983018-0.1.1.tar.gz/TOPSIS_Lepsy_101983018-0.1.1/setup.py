import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS_Lepsy_101983018", # Replace with your own username
    version="0.1.1",
    author="Lepsy Goyal",
    author_email="goyalpti99@gmail.com",
    description="This library gives function of save_topsis to give analysis...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)