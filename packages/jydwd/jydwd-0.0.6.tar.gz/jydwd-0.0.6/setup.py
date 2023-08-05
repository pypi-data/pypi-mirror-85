from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="jydwd", # Replace with your own username
    version="0.0.6",
    author="jiangyd",
    keywords="jydwd",
    author_email="962584902@qq.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    install_requires=["requests>=2.23.0"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)