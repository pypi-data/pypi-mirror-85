import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hpogrid", # Replace with your own username
    version="0.8.2.3",
    author="Alkaid Cheng",
    author_email="chi.lung.cheng@cern.ch",
    description="A workflow for hyperparamter optimization using the ATLAS grid resources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/aml/hyperparameter-optimization/alkaid-qt/hpogrid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[   
          'ray[tune]',
          'pandas',
          'tqdm',
          'tabulate',
          'numpy',
          'psutil'
      ],
    scripts=['bin/hpogrid'],
    python_requires='>=3.7',
)
