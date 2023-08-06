import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="manim-ext",
    version="0.0.1",
    author="Roopes OR",
    author_email="roopeshor6@gmail.com",
    description="A small package containing useful functions and classes for creating manim(ce) animations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Roopesh2/manim-ext",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)