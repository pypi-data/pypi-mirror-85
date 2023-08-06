import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-sqlalchemy-extended",
    version="0.0.12",
    author="luanws",
    author_email="luan.w.silveira@gmail.com",
    description="SQLAlchemy autocomplete",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luanws/flask-sqlalchemy-extended",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)