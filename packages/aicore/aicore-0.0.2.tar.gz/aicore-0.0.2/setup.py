import pathlib

import setuptools


def read(HERE: pathlib.Path, filename, variable):
    namespace = {}

    exec(open(HERE / "aicore" / filename).read(), namespace)  # get version
    return namespace[variable]


HERE = pathlib.Path(__file__).resolve().parent

setuptools.setup(
    name="aicore",
    version=read(HERE, pathlib.Path("_version.py"), "__version__"),
    author="theaicore",
    author_email="admissions@theaicore.com",
    description="Library for CoreAI courses (https://www.theaicore.com/)",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://www.theaicore.com/",
    packages=setuptools.find_packages(),
    install_requires=["numpy>=1.19.4"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Website": "https://www.theaicore.com/",
    },
    keywords="theaicore aicore course machine learning deep learning",
)
