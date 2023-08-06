from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="TOPSIS_Ankush_101803384",
    version="0.1.0",
    description = 'Implementation of TOPSIS',
    author="Ankush Gupta",
    author_email="ankushgupta10092000@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["TOPSIS_Ankush_101803384"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data = True,
    python_requires='>=3.0',
    keywords='topsis pandas rank decision_matrix ',
    install_requires=['pandas'],
)