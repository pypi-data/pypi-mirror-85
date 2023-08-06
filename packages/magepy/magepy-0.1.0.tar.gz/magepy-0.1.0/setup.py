import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="magepy",
    version="0.1.0",
    author="Stage 2 Security",
    author_email="magepy@stage2sec.com",
    description="An SDK to interact with MAGE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Stage2Sec/magepy",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'python-dotenv>=0.15.0',
        'sgqlc>=11.0',
        'warrant>=0.6.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
