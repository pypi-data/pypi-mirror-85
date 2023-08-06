import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pumml",
    version="0.0.2",
    author="Nathan C. Frey, Jin Wang",
    maintainer="Nathan C. Frey",
    author_email="n.frey@seas.upenn.edu",
    description="Positive and Unlabeled Materials Machine Learning (pumml) is a code that uses semi-supervised positive and unlabeled (PU) machine learning to classify materials when data is incomplete and only examples of 'positive' materials are available.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncfrey/pumml",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['matplotlib>=3.1.1', 'monty>=2.0.4', 'numpy==1.19.4', 'pandas==1.1.4', 'scikit-learn==0.23.2', 'scipy>=1.3.0', 'seaborn>=0.9.0',
        'matminer==0.6.3',
        'pymatgen==2020.11.11'],
    keywords=["VASP", "machine", "learning", "materials", "science", "DFT", "synthesis"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
