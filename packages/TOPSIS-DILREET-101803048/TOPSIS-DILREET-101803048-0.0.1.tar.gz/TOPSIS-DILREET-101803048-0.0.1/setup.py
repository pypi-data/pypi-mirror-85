import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS-DILREET-101803048", # Replace with your own username
    version="0.0.1",
    author="DILREET SINGH",
    author_email="coderprodigy@gmail.com",
    description="TOPSIS is an acronym that stands for â€˜Technique of Order Preference Similarity to the Ideal Solutionâ€™ and is a pretty straightforward MCDA method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coderprodigy/TOPSIS-DILREET-101803048",
    packages = ['TOPSIS-DILREET-101803048'],   
    # packages=setuptools.find_packages(),
    install_requires=[ 'numpy','pandas',],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
