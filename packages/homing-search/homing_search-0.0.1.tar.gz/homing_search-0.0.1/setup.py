import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="homing_search",
    version="0.0.1",
    author="Andrew de Jonge",
    author_email="talkingtoaj@hotmail.com",
    description="Smart hyperparameter optimization in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/talkingtoaj/homing_search",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.6',
)