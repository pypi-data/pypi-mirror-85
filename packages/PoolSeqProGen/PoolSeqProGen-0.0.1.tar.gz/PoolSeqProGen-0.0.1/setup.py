import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PoolSeqProGen", 
    version="0.0.1",
    author="Rigbe G. Weldatsadik",
    author_email="rigbe.weldatsadik@helsinki.fi",
    description="A package for creating variant protein databases for bacteria from Pool-seq experiments ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RigbeGW/poolseq_variantdb",
    packages=setuptools.find_packages(include=['PoolSeqProGen', 'PoolSeqProGen.*']),
    install_requires=[
        'pyteomics',
        'biopython',
        'pysam',
        
    ],
    entry_points={
        'console_scripts': ['generate_variants=PoolSeqProGen.generate_variants:main']
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7,>=3.3',
)