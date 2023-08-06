import setuptools

def readme():
    with open('README.md') as file:
        README = file.read()
    return README

setuptools.setup(
    name="TOPSIS-Aseem-101803469",
    version="3.0.2",
    description="A Python package for implementing TOPSIS technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Aseem Khullar",
    author_email="akhullar_be18@thapar.edu",
    url = 'https://pypi.org/project/TOPSIS-Aseem-101803469/',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: 3.7"
    ],
    packages=["src"],
    include_package_data=True,
    install_requires=['scipy',
                      'tabulate',
                      'numpy',
                      'pandas',
     ],
     entry_points={
        "console_scripts": [
            "topsis=src.topsis:main",
        ]
     },
)
