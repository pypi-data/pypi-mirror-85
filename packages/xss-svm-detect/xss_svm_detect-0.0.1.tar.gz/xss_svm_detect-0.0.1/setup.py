import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xss_svm_detect",
    version="0.0.1",
    author="SJLiu",
    author_email="liu.so@northeastern.edu",
    description="A SVM mode for detect xss payload",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.ccs.neu.edu/Capstone-Team/svm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)