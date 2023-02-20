from setuptools import setup
with open("README.md") as file:
    readme_content = file.read()

setup(
    name="dexonline-api",
    version="1.0.0",
    description="Unofficial dexonline.ro API",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    url="https://github.com/radu781/Dexonline-API",
    author="Radu-Alexandru Popa",
    author_email="poparadu501@gmail.com",
    license="MIT",
    packages=["dexonline_api"],
    install_requires=["beautifulsoup4", "requests"],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
