import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visanz",
    version="0.0.1",
    author="Simeon, Emil, Joel",
    author_email="",
    description="Package for linking historic Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joelosw/VisualAnzeights",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
