from setuptools import setup


setup(
    name="topsis_kritika_101983031", # Replace with your own username
    version="0.8",
    author="kritika aggarwal",
    author_email="kritikaaggarwal1621@gmail.com",
    description="python implementation for TOPSIS",
    long_description='''TOPSIS_kritika_101983031 implementation of Technique of Order Preference Similarity to the Ideal Solution. it is based on finding an ideal and an anti-ideal solution and comparing the distance of each one of the alternatives to those.
    to run from command line:
following format must be followed:
Usages:
python topsis.py <InputDataFile> <Weights> <Impacts> <ResultFileName>
Example:
python topsis.py inputfile.csv “1,1,1,2” “+,+,-,+” result.csv''',
    long_description_content_type="text/markdown",
    url="https://github.com/kritsid/TOPSIS-kritika-101983031",
    packages=["topsis_kritika_101983031"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['scipy',
                      'tabulate',
                      'numpy',
                      'pandas'
     ],
    
)