from setuptools import setup


setup(
    name="TOPSIS_Ankush_101803384",
    version="0.0.1",
    description = 'Implementation of TOPSIS',
    author="Ankush Gupta",
    author_email="ankushgupta10092000@gmail.com",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/TOPSIS_AyushJain",
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