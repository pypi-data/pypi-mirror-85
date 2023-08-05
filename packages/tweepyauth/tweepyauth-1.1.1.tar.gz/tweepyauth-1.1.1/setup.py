import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tweepyauth",
    version="1.1.1",
    author="mocchapi",
    author_email="mocchapi@gmail.com",
    description="A small library to ease tweepy authentication",
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=['tweepy'],
    url="https://gitlab.com/mocchapi/tweepyauth",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)