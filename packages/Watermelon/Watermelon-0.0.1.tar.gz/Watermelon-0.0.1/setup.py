import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Watermelon", # Replace with your own username
    version="0.0.1",
    author="Harsha",
    author_email="harsha7addanki@gmail.com",
    description="Like Pickle But For Files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harsha7addanki/watermelon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)