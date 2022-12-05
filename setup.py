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
    install_requires=[
        "mpi4py>=2.0",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)
