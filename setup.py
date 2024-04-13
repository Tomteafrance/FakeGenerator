import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fake_generator",
    version="0.0.0",
    author="Tom TEA",
    author_email="tomteafrance@gmail.com",
    description="fake generator package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.7,<3.11',
    keywords=["Python", "Faker"],
    install_requires = [
        "Faker >= 22.0.0",
        "pandas >= 2.0.2"
    ],
)
