import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="steinloss",  # Replace with your own username
    version="0.0.1",
    author="Steinwurf ApS",
    author_email="contact@steinwurf.com",
    description="Package loss measuring tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/steinwurf/steinloss",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Dash"

    ],
    python_requires='>=3.8',
)
