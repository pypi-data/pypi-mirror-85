import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Folders",  # Replace with your own username
    version="0.0.1",
    author="Sina Khalili",
    author_email="sina@sinakhalili.com",
    description="An interpreter for the Folders esolang",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SinaKhalili/Folders.py",
    packages=setuptools.find_packages(exclude=("tests")),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "Folders=folders.__init__:main"
        ]
    }
)
