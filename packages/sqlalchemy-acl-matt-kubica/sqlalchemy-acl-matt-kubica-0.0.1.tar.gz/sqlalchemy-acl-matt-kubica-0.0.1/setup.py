import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlalchemy-acl-matt-kubica",
    version="0.0.1",
    author="Mateusz Kubica",
    author_email="mateusz.kubica99@gmail.com",
    description="Acces List library for SQLAlchemy ORM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matt-kubica/sqlalchemy-acl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.6',
)