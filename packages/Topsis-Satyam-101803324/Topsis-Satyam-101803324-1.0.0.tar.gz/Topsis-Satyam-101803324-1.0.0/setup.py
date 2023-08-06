
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Topsis-Satyam-101803324",
    version="1.0.0",
    license='MIT',
    author="Satyam Verma",
    author_email="satyamv069@gmail.com",
    description="This package can be used to calculate the topsis score of multiple component data and rank them accordingly",
    long_description=long_description,
    url='https://coe1316.ml',
    long_description_content_type="text/markdown",
    keywords = ['TOPSIS'],  
    install_requires=[           
          'pandas',
          'numpy'
      ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',     
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
) 
