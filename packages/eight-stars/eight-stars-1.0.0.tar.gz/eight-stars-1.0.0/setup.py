from setuptools import find_packages, setup

setup(
    name="eight-stars",
    version="1.0.0",
    author="Robert Ganowski",
    author_email="robert.ganowski@gmail.com",
    description="Simple stars geometries",
    long_description="For longer description, please visit project [home page](https://github.com/rganowski/eight-stars)",
    long_description_content_type="text/markdown",
    url="https://github.com/rganowski/eight-stars",
    platforms="Posix; MacOS X; Windows",
    packages=find_packages(where="./src"),
    license="MIT",
    package_dir={
        "": "src"
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
