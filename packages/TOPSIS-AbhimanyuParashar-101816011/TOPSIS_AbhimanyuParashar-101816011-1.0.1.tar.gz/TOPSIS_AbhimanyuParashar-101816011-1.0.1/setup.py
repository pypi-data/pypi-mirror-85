from setuptools import setup

setup(
    name="TOPSIS_AbhimanyuParashar-101816011",
    version="1.0.1",
    description="This is a Python package to implement TOPSIS technique.",
    author="Abhimanyu Parashar",
    author_email="aparashar1_be18@thapar.edu",
    url = 'https://pypi.org/project/TOPSIS-AbhimanyuParashar-101816011',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7",
    ],
    packages=["source"],
    include_package_data=True,
    install_requires=['scipy',
                      'tabulate',
                      'numpy',
                      'pandas',
     ],
     entry_points={
        "console_scripts": [
            "topsis=source.topsis:main",
        ]
     },
)
