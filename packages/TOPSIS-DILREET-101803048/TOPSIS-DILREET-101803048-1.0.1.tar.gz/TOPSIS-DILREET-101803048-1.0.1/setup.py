import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="TOPSIS-DILREET-101803048", 
    version="1.0.1",
    author="DILREET SINGH",
    author_email="coderprodigy@gmail.com",
    description="TOPSIS is an acronym that stands for â€˜Technique of Order Preference Similarity to the Ideal Solutionâ€™ and is a pretty straightforward MCDA method",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/coderprodigy/TOPSIS-DILREET-101803048",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    # Folder  from which I will create the distribution file
    packages = ['TOPSIS-DILREET-101803048'],    
    include_package_data=True,
    install_requires=['pandas','numpy==1.19.3'],
    # entry_points={
    #     "console_scripts": [
    #         "square=square.__main__:main",
    #     ]
    # },
)


# from setuptools import se tup

# with open("README.md","r") as fh:
#     long_description =fh.read()

# setup(
#     name="TOPSIS-DILREET-101803048-v2", 
#     version="1.0.1",
#     author="DILREET SINGH",
#     author_email="coderprodigy@gmail.com",
#     description="TOPSIS is an acronym that stands for â€˜Technique of Order Preference Similarity to the Ideal Solutionâ€™ and is a pretty straightforward MCDA method",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/coderprodigy/TOPSIS-DILREET-101803048",
#     packages = ['TOPSIS-DILREET-101803048'],   
#     # packages=setuptools.find_packages(),
#     install_requires=[ 'numpy','pandas',],
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
# )

