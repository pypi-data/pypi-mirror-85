import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spongebox", # 届时使用pip install {}的包名
    version="0.3.0",
    author="spongebob",
    author_email="author@example.com",
    description="A high-level wrapped tool-chest with frequently-used functionalities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/23spongebob/spongebox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
