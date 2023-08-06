
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Topsis-Satyam-101803324",
    version="1.0.5",
    license='MIT',
    author="Satyam Verma",
    author_email="satyamv069@gmail.com",
    description="This package can be used to calculate the topsis score of multiple component data and rank them accordingly",
    long_description=long_description,
    url='https://pypi.org/project/Topsis-Satyam-101803324',
    long_description_content_type="text/markdown",
    keywords = ['TOPSIS'],  
    install_requires=[           
          'pandas',
          'numpy'
      ],
    packages=['source'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',     
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        "console_scripts": [
            "topsis=source.main:topsis",
        ]
     },
) 
