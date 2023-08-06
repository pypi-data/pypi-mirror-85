import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SF_Mako",
    version="0.0.0.12",
    author="Mark Cartagena",
    author_email="mark@mknxgn.com",
    description="MkNxGn SF Mako",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mknxgn.com/",
    install_requires=['mknxgn_essentials>=0.1.35.12'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
