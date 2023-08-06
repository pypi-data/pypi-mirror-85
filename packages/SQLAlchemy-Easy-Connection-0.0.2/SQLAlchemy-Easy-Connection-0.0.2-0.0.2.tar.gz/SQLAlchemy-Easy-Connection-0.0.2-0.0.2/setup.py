import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SQLAlchemy-Easy-Connection-0.0.2",  # Replace with your own username
    version="0.0.2",
    author="Marcus Paiva",
    author_email="marcus.paiva.ti@gmail.com",
    description="Simple way to connect Database using SQLAlchemy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarcusPaiva/SQLAlchemy-Easy-Connection.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["sqlalchemy"],
)
