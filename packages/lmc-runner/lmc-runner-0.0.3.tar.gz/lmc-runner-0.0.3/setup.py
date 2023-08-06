import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lmc-runner",
    version="0.0.3",
    author="dhruvnps",
    description="Run LMC assembly code!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhruvnps/lmc-runner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['lmc-runner=lmc_runner.__init__:run'],
    },
    python_requires='>=3.6',
)
