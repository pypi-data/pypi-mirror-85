import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kartik_takyar", # Replace with your own username
    version="0.0.1",
    author="Kartik Takyar",
    author_email="kartiktakyar6@gmail.com",
    description="TOPSIS Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KartikTakyar0046",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)