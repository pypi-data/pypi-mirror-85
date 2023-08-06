import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spotiply",
    version="1.0.0",
    author="muggleboii",
    author_email="francisgian.fgm@gmail.com",
    description="A Python Library for Spotify Web API.\
 This is a self project while expanding my\
 knowledge in Python.",
    long_description=long_description,
    packages=setuptools.find_packages(),
    long_description_content_type="text/markdown",
    install_requires=["requests==2.24.0"],
    url="https://github.com/muggleboii/spotify",
    python_requires='>=3.6',
)
