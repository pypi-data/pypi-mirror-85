import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Pre_processor", # Replace with your own username
    version="0.0.3",
    author="Neeraj Kumar",
    author_email="ndevsinha@gmail.com",
    description="csv and json file preprocessor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ndevsinha/Pre_processor",
    download_url = "https://github.com/ndevsinha/Pre_processor/archive/v_0.0.2.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
