import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="progress-keeper",
    version="0.0.1",
    author="Anders Bergman",
    author_email="",
    description="Stores progress in a file, useful for idempotent multi-step processes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndoKalrisian/progress-keeper",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['configparser'],
    license="MIT License"
)
