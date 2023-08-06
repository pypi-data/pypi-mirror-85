from setuptools import setup
 
with open("README.md", "r") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setup(
    name="Topsis-Kashish-101983051",
    version="1.1.0",
    description="Implementation of Topsis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kashish Mehra",
    author_email="kashishmehra50@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=['pandas',
                      'numpy'],
     setup_requires=['wheel']
)