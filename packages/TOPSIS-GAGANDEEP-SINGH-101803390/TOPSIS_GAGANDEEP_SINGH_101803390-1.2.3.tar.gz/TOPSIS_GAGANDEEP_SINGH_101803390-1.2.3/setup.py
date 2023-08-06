import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS_GAGANDEEP_SINGH_101803390", # Replace with your own username
    version="1.2.3",
    author="Gagandeep Singh",
    author_email="gagan.gagan211@gmail.com",
    description="This library gives function of save_topsis to give analysis...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Steveroger5/TOPSIS_GAGANDEEP_101803390",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)