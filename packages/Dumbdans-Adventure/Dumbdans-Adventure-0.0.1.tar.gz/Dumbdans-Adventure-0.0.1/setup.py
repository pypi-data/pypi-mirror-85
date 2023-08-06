import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Dumbdans-Adventure",
    version="0.0.1",
    author="Álef Ádonis",
    author_email="alef.carlos@ccc.ufcg.edu.br",
    description="Arcade game made with pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlefAdonis/Dumbdan-Game",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
