import setuptools
import os


readme_dir = os.path.dirname(__file__)
readme_path = os.path.join(readme_dir, 'README.md')
with open(readme_path, "r") as f:
    long_description = f.read()


required_packages = [
    "scikit-learn>=0.23.2",
    "numpy>=1.19.4",
    "pandas>=1.1.4",
    "proteinko==5.0",
    "joblib>=0.17.0",
    'argparse'
]


setuptools.setup(
    name="mhclovac",
    version="3.0",
    author="Stefan Stojanovic",
    author_email="stefs304@gmail.com",
    description="MHC class I binding and epitope prediction based on modeled "
                "physicochemical properties of peptides",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/stojanovicbg/mhclovac",
    packages=[
        'mhclovac',
    ],
    package_data={
        'mhclovac': ['index/*', 'models/*']
    },
    install_requires=required_packages,
    entry_points={
          'console_scripts': [
              "mhclovac=mhclovac.run:run",
          ]
    },
    classifiers=(
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    )
)
