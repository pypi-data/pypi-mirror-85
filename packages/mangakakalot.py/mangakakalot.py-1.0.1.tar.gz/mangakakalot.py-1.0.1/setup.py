import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mangakakalot.py",
    version="1.0.1",
    author="webuby",
    author_email="",
    description="mangakakalot.py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/webuby/mangakakalot.py",
    keywords="manga mangakakalot mangakakalot.py anime mangakakalot.py",
    packages=setuptools.find_packages(),
    install_requires=["requests", "beautifulsoup4", "Pillow"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
