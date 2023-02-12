from setuptools import setup

setup(
    name="dexonline",
    version="1.0.0",
    description="Unofficial dexonline.ro API",
    url="",
    author="Radu-Alexandru Popa",
    author_email="poparadu501@gmail.com",
    license="MIT",
    packages=["dexonline"],
    install_requires=["beautifulsoup4==4.11.1"],
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)
