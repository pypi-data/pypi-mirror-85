import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LibrasLib",
    version="0.0.1",
    author="Amanda Batista Medeiros",
    author_email="amandamedeiros.ufsc@gmail.com",
    description="Biblioteca de interpretação em LIBRAS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amanemedeiros/libraslib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8",
)