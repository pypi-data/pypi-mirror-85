from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="data-profile-viewer",
    version="0.2.3",
    author="Sonia Castelo",
    author_email="s.castelo@nyu.edu",
    description="Data Profile Viewer tool. Enables the exploration of data profile in Jupyter Notebooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soniacq/DataProfileVis",
    packages=find_packages(exclude=['js', 'node_modules']),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "python-dateutil",
        "numpy",
        "scipy",
        "scikit-learn",
        "networkx",
        "notebook",
        "datamart_profiler==0.8.1"
    ]
)
