import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-kapnoc",  # Replace with your own username
    version="0.0.3",
    author="Tanguy Gérôme",
    author_email="tanguy.gerome@gmail.com",
    description="Personnal helpers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://kapno.cc",
    packages=setuptools.find_packages(),
    license="BSD-3-Clause",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
    install_requires=[
        "Pillow",
        "martor",
        "easy-thumbnails",
    ],
    python_requires='>=3.6',
)
