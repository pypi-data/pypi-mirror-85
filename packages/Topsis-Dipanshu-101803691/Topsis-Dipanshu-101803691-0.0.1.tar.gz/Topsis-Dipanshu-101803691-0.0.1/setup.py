import setuptools
with open("README.md", "r") as fh:
    long = fh.read()
setuptools.setup(
    name="Topsis-Dipanshu-101803691",
    version="0.0.1",
    author="	Dipanshu Golan",
    author_email="dipanshugolan96@gmail.com",
    description="it is package which tells you best value based on the data by using some mathematical calculations",
    long_description=long,
    long_description_content_type="text/markdown",
    py_modules=["topsis"],
    package_dir={'':'topsis_package'},
    url="https://github.com/DipanshuGolan96/topsis",	   
    install_requires=['pandas','numpy==1.19.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
