import setuptools

def readme():
    with open('README.md') as file:
        README = file.read()
    return README

setuptools.setup(
    name="TOPSIS-Dhruv-101803466",
    version="3.0.2",
    description="TOPSIS implementation.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Dhruv Bansal",
    author_email="dbansal_be18@thapar.edu",
    url = 'https://pypi.org/project/TOPSIS-Dhruv-101803466/',
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
