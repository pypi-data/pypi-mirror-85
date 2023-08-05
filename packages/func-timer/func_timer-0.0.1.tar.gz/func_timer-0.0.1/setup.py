import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="func_timer",  # Replace with your own username
    version="0.0.1",
    author="zqsc",
    author_email="zhao_zqsc@sina.com",
    description="A small example package, used for timing function",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zqsc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
